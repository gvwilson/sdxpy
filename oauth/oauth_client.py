"""OAuth 2.0 Client implementation."""

from asimpy import Process, Queue
from typing import Optional, List
from oauth_types import (
    AuthorizationRequest,
    TokenRequest,
    ResourceRequest,
    TokenResponse,
    generate_token,
)
from authorization_server import AuthorizationServer
from resource_server import ResourceServer


# mccole:init
class OAuthClient(Process):
    """OAuth 2.0 client application."""

    def init(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        auth_server: AuthorizationServer,
        resource_server: ResourceServer,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_server = auth_server
        self.resource_server = resource_server

        self.access_token: Optional[str] = None

        print(f"[{self.now:.1f}] Client '{client_id}' started")
    # mccole:/init

    # mccole:run
    async def run(self):
        """Demonstrate complete OAuth flow."""
        # Step 1: Request authorization
        scopes = ["profile", "photos"]
        code = await self.request_authorization(scopes)

        if not code:
            print(f"[{self.now:.1f}] Client: Authorization failed")
            return

        # Step 2: Exchange code for token
        token_response = await self.exchange_code_for_token(code)

        if not token_response or token_response.token_type == "error":
            print(f"[{self.now:.1f}] Client: Token exchange failed")
            return

        self.access_token = token_response.access_token
        print(f"[{self.now:.1f}] Client: Got access token!")

        # Step 3: Access protected resources
        await self.timeout(0.5)
        await self.access_resource("/api/profile")

        await self.timeout(0.5)
        await self.access_resource("/api/photos")

        # Try accessing resource without permission
        await self.timeout(0.5)
        await self.access_resource("/api/messages")
    # mccole:/run

    # mccole:request_auth
    async def request_authorization(self, scopes: List[str]) -> Optional[str]:
        """Step 1: Request user authorization."""
        print(f"[{self.now:.1f}] Client: Requesting authorization for {scopes}")

        state = generate_token("state")  # CSRF protection
        response_queue = Queue(self._env)

        request = AuthorizationRequest(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=scopes,
            state=state,
            response_queue=response_queue,
        )

        await self.auth_server.auth_queue.put(request)
        response = await response_queue.get()

        # Validate state to prevent CSRF
        if response.state != state:
            print(f"[{self.now:.1f}] Client: State mismatch - possible CSRF attack!")
            return None

        print(f"[{self.now:.1f}] Client: Received authorization code")
        return response.code
    # mccole:/request_auth

    # mccole:exchange_code
    async def exchange_code_for_token(self, code: str) -> Optional[TokenResponse]:
        """Step 2: Exchange authorization code for access token."""
        print(f"[{self.now:.1f}] Client: Exchanging code for token")

        response_queue = Queue(self._env)

        request = TokenRequest(
            code=code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            response_queue=response_queue,
        )

        await self.auth_server.token_queue.put(request)
        response = await response_queue.get()

        return response
    # mccole:/exchange_code

    # mccole:access_resource
    async def access_resource(self, path: str):
        """Step 3: Access protected resource with token."""
        print(f"[{self.now:.1f}] Client: Accessing {path}")

        if not self.access_token:
            print(f"[{self.now:.1f}] Client: No access token!")
            return

        response_queue = Queue(self._env)

        request = ResourceRequest(
            access_token=self.access_token,
            resource_path=path,
            response_queue=response_queue,
        )

        await self.resource_server.resource_queue.put(request)
        response = await response_queue.get()

        if response.success:
            print(f"[{self.now:.1f}] Client: Success! Data: {response.data}")
        else:
            print(f"[{self.now:.1f}] Client: Failed - {response.error}")
    # mccole:/access_resource
