"""OAuth 2.0 Client Credentials flow (machine-to-machine).

The Client Credentials flow is used when the *application itself* is the resource owner—
there is no human user to authenticate.  Examples:
  - A batch job that reads from a data warehouse API.
  - A microservice that calls another microservice.
  - A scheduled task that posts to an analytics endpoint.

The flow has two steps:
  1. The client sends its client_id and client_secret directly to the token endpoint.
  2. The authorization server issues an access token.
  There is no authorization code, no redirect URI, and no user consent screen.

This is simpler than the authorization code flow, but the client_secret must
be protected carefully—it acts as the application's password.
"""

from asimpy import Process, Queue
from typing import Optional


# mccole:cc_token_request
from dataclasses import dataclass


@dataclass
class ClientCredentialsRequest:
    """Token request for the client credentials flow.

    Unlike an authorization code request, there is no code to exchange.
    The client authenticates directly with its credentials.
    """

    client_id: str
    client_secret: str
    scope: list[str]
    response_queue: Queue
# mccole:/cc_token_request


# mccole:cc_client
class ClientCredentialsClient(Process):
    """OAuth client using the client credentials flow.

    Suitable for server-to-server communication where there is no user.
    The client authenticates itself and receives a token that represents
    the application's own identity rather than any particular user.
    """

    def init(
        self,
        client_id: str,
        client_secret: str,
        auth_server_token_queue: Queue,
        scopes: Optional[list[str]] = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_server_token_queue = auth_server_token_queue
        self.scopes = scopes or ["read"]

        self.access_token: Optional[str] = None
        self.token_expiry: float = 0.0

        print(
            f"[{self.now:.1f}] M2M client '{client_id}' started "
            f"(scopes: {self.scopes})"
        )

    async def run(self) -> None:
        """Acquire a token and use it; refresh when it expires."""
        await self._acquire_token()
        if self.access_token:
            print(
                f"[{self.now:.1f}] M2M client: Token acquired, "
                f"making API calls..."
            )
            # Simulate periodic API calls.
            for _ in range(3):
                await self.timeout(1.0)
                await self._make_api_call()
        else:
            print(f"[{self.now:.1f}] M2M client: Failed to acquire token")

    async def _acquire_token(self) -> None:
        """Request a token directly from the token endpoint."""
        print(f"[{self.now:.1f}] M2M client: Requesting token with client credentials")

        response_queue: Queue = Queue(self._env)
        request = ClientCredentialsRequest(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scopes,
            response_queue=response_queue,
        )
        await self.auth_server_token_queue.put(request)
        response = await response_queue.get()

        if hasattr(response, "access_token") and response.access_token:
            self.access_token = response.access_token
            self.token_expiry = self.now + 60.0   # tokens typically last 1 hour
            print(
                f"[{self.now:.1f}] M2M client: Token acquired "
                f"(expires at {self.token_expiry:.0f})"
            )
        else:
            print(f"[{self.now:.1f}] M2M client: Token request failed")

    async def _make_api_call(self) -> None:
        """Make an API call, refreshing the token if it has expired."""
        if self.now >= self.token_expiry:
            print(f"[{self.now:.1f}] M2M client: Token expired, refreshing...")
            await self._acquire_token()

        if self.access_token:
            print(
                f"[{self.now:.1f}] M2M client: API call with token "
                f"{self.access_token[:8]}..."
            )
        else:
            print(f"[{self.now:.1f}] M2M client: Cannot call API, no token")
# mccole:/cc_client
