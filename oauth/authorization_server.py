"""OAuth 2.0 Authorization Server implementation."""

from asimpy import Process, Queue, FirstOf
from typing import Dict, List
from oauth_types import (
    AuthorizationRequest,
    AuthorizationResponse,
    TokenRequest,
    TokenResponse,
    AuthorizationCode,
    AccessToken,
    generate_token,
)


# mccole:init
class AuthorizationServer(Process):
    """OAuth 2.0 authorization server."""

    def init(self):
        self.auth_queue = Queue(self._env)
        self.token_queue = Queue(self._env)

        # Registered clients
        self.clients: Dict[str, Dict] = {}

        # Issued authorization codes
        self.auth_codes: Dict[str, AuthorizationCode] = {}

        # Issued access tokens
        self.access_tokens: Dict[str, AccessToken] = {}

        # User credentials (simplified - real systems use secure storage)
        self.users = {
            "alice@example.com": "password123",
            "bob@example.com": "secret456",
        }

        print(f"[{self.now:.1f}] Authorization Server started")
    # mccole:/init

    # mccole:register
    def register_client(
        self, client_id: str, client_secret: str, redirect_uris: List[str]
    ):
        """Register a new OAuth client."""
        self.clients[client_id] = {
            "secret": client_secret,
            "redirect_uris": redirect_uris,
        }
        print(f"[{self.now:.1f}] Registered client: {client_id}")
    # mccole:/register

    # mccole:run
    async def run(self):
        """Main server loop."""
        while True:
            # Handle both authorization and token requests
            name, request = await FirstOf(
                self._env, auth=self.auth_queue.get(), token=self.token_queue.get()
            )

            if name == "auth":
                await self.handle_authorization_request(request)
            elif name == "token":
                await self.handle_token_request(request)
    # mccole:/run

    # mccole:handle_auth
    async def handle_authorization_request(self, request: AuthorizationRequest):
        """Handle authorization request from client."""
        print(f"[{self.now:.1f}] AuthServer: Received {request}")

        if not self._validate_auth_request(request):
            return

        # Simulate user authentication and consent
        await self.timeout(0.5)  # User login time
        print(f"[{self.now:.1f}] AuthServer: User authenticated, showing consent")

        await self.timeout(0.3)  # User consent time
        print(f"[{self.now:.1f}] AuthServer: User granted permissions: {request.scope}")

        await self._issue_authorization_code(request)
    # mccole:/handle_auth

    # mccole:validate_auth
    def _validate_auth_request(self, request: AuthorizationRequest) -> bool:
        """Check that the client is registered and the redirect URI is allowed."""
        if request.client_id not in self.clients:
            print(f"[{self.now:.1f}] AuthServer: Unknown client {request.client_id}")
            return False

        client = self.clients[request.client_id]
        if request.redirect_uri not in client["redirect_uris"]:
            print(f"[{self.now:.1f}] AuthServer: Invalid redirect URI")
            return False

        return True
    # mccole:/validate_auth

    # mccole:issue_code
    async def _issue_authorization_code(self, request: AuthorizationRequest):
        """Generate, store, and return a one-time authorization code."""
        code = generate_token("code")
        auth_code = AuthorizationCode(
            code=code,
            client_id=request.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            expires_at=self.now + 600,  # 10 minute expiry
        )
        self.auth_codes[code] = auth_code

        response = AuthorizationResponse(code=code, state=request.state)
        await request.response_queue.put(response)

        print(f"[{self.now:.1f}] AuthServer: Issued authorization code")
    # mccole:/issue_code

    # mccole:handle_token
    async def handle_token_request(self, request: TokenRequest):
        """Exchange authorization code for access token."""
        print(f"[{self.now:.1f}] AuthServer: Received {request}")

        auth_code = await self._validate_token_request(request)
        if auth_code is None:
            return

        await self._issue_access_token(request, auth_code)
    # mccole:/handle_token

    # mccole:validate_token
    async def _validate_token_request(
        self, request: TokenRequest
    ) -> AuthorizationCode | None:
        """Validate client credentials and authorization code; return code or None."""
        error = TokenResponse(access_token="", token_type="error")

        if request.client_id not in self.clients:
            print(f"[{self.now:.1f}] AuthServer: Unknown client")
            await request.response_queue.put(error)
            return None

        client = self.clients[request.client_id]
        if client["secret"] != request.client_secret:
            print(f"[{self.now:.1f}] AuthServer: Invalid client secret")
            await request.response_queue.put(error)
            return None

        if request.code not in self.auth_codes:
            print(f"[{self.now:.1f}] AuthServer: Invalid authorization code")
            await request.response_queue.put(error)
            return None

        auth_code = self.auth_codes[request.code]

        if not auth_code.is_valid(self.now):
            print(f"[{self.now:.1f}] AuthServer: Authorization code expired or used")
            await request.response_queue.put(error)
            return None

        if auth_code.client_id != request.client_id:
            print(f"[{self.now:.1f}] AuthServer: Code issued to different client")
            await request.response_queue.put(error)
            return None

        if auth_code.redirect_uri != request.redirect_uri:
            print(f"[{self.now:.1f}] AuthServer: Redirect URI mismatch")
            await request.response_queue.put(error)
            return None

        return auth_code
    # mccole:/validate_token

    # mccole:issue_token
    async def _issue_access_token(
        self, request: TokenRequest, auth_code: AuthorizationCode
    ):
        """Mark the code used, generate an access token, store it, and send it."""
        auth_code.used = True

        access_token = generate_token("access")
        token = AccessToken(
            token=access_token,
            client_id=request.client_id,
            scope=auth_code.scope,
            expires_at=self.now + 3600,  # 1 hour expiry
        )
        self.access_tokens[access_token] = token

        response = TokenResponse(
            access_token=access_token,
            token_type="Bearer",
            expires_in=3600,
            scope=auth_code.scope,
        )
        await request.response_queue.put(response)

        print(f"[{self.now:.1f}] AuthServer: Issued access token")
    # mccole:/issue_token
