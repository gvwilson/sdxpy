"""OAuth 2.0 Resource Server implementation."""

from asimpy import Process, Queue
from oauth_types import AccessToken, ResourceRequest, ResourceResponse
from authorization_server import AuthorizationServer


# mccole:init
class ResourceServer(Process):
    """OAuth 2.0 resource server (protected API)."""

    def init(self, auth_server: AuthorizationServer):
        self.auth_server = auth_server
        self.resource_queue = Queue(self._env)

        # Protected resources
        self.resources = {
            "/api/profile": {
                "scope_required": ["profile"],
                "data": {"name": "Alice", "email": "alice@example.com"},
            },
            "/api/photos": {
                "scope_required": ["photos"],
                "data": {"photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg"]},
            },
            "/api/messages": {
                "scope_required": ["messages"],
                "data": {"messages": ["Hello!", "How are you?"]},
            },
        }

        print(f"[{self.now:.1f}] Resource Server started")
    # mccole:/init

    # mccole:run
    async def run(self):
        """Main server loop."""
        while True:
            request = await self.resource_queue.get()
            await self.handle_resource_request(request)
    # mccole:/run

    # mccole:handle_resource
    async def handle_resource_request(self, request: ResourceRequest):
        """Handle API request with access token."""
        print(f"[{self.now:.1f}] ResourceServer: Received {request}")

        token = await self._validate_token(request)
        if token is None:
            return

        resource = await self._check_resource_access(request, token)
        if resource is None:
            return

        print(f"[{self.now:.1f}] ResourceServer: Returning {request.resource_path}")
        await request.response_queue.put(
            ResourceResponse(success=True, data=resource["data"])
        )
    # mccole:/handle_resource

    # mccole:validate_token
    async def _validate_token(
        self, request: ResourceRequest
    ) -> AccessToken | None:
        """Check that the token exists and has not expired; send error if not."""
        if request.access_token not in self.auth_server.access_tokens:
            print(f"[{self.now:.1f}] ResourceServer: Invalid token")
            await request.response_queue.put(
                ResourceResponse(success=False, error="invalid_token")
            )
            return None

        token = self.auth_server.access_tokens[request.access_token]

        if not token.is_valid(self.now):
            print(f"[{self.now:.1f}] ResourceServer: Token expired")
            await request.response_queue.put(
                ResourceResponse(success=False, error="token_expired")
            )
            return None

        return token
    # mccole:/validate_token

    # mccole:check_access
    async def _check_resource_access(
        self, request: ResourceRequest, token: AccessToken
    ) -> dict | None:
        """Check that the resource exists and the token's scope covers it."""
        if request.resource_path not in self.resources:
            print(f"[{self.now:.1f}] ResourceServer: Resource not found")
            await request.response_queue.put(
                ResourceResponse(success=False, error="not_found")
            )
            return None

        resource = self.resources[request.resource_path]
        required_scopes = set(resource["scope_required"])
        token_scopes = set(token.scope)

        if not required_scopes.issubset(token_scopes):
            print(f"[{self.now:.1f}] ResourceServer: Insufficient scope")
            await request.response_queue.put(
                ResourceResponse(success=False, error="insufficient_scope")
            )
            return None

        return resource
    # mccole:/check_access
