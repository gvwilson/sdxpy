"""OAuth 2.0 Authorization Code flow with PKCE.

PKCE (Proof Key for Code Exchange, RFC 7636) protects the authorization code
flow against interception attacks on mobile and single-page apps.

The problem PKCE solves:
  Mobile apps and single-page apps cannot securely store a client secret,
  so they cannot authenticate themselves to the token endpoint the way
  a server-side app can.  An attacker who intercepts the authorization code
  (e.g., via a malicious app registered for the same URI scheme) could
  exchange it for a token.

How PKCE works:
  1. The client generates a random *code verifier* (43-128 random chars).
  2. It hashes the verifier with SHA-256 and base64url-encodes the hash
     to produce the *code challenge*.
  3. It sends the code challenge (not the verifier) in the authorization request.
  4. The authorization server stores the challenge with the code.
  5. When exchanging the code for a token, the client sends the original verifier.
  6. The server hashes the verifier and compares to the stored challenge.
     Only the client that created the code challenge can complete the exchange,
     because only it knows the original verifier.

An interceptor who steals the authorization code cannot use it without knowing
the verifier, which was never transmitted over the network.

Token storage note:
  Access tokens and refresh tokens must be stored securely by the client.
  On mobile apps, use the platform's secure storage (iOS Keychain, Android Keystore).
  In browsers, prefer sessionStorage (not localStorage) for short-lived tokens,
  and never store tokens in cookies without the HttpOnly and Secure flags.
  A token stored in localStorage is accessible to any JavaScript on the page,
  including third-party scripts, which is equivalent to storing a password in plaintext.
"""

import hashlib
import base64
import os
from asimpy import Process, Queue
from typing import Optional
from oauth_types import generate_token, TokenResponse


# mccole:pkce_helpers
def generate_code_verifier(length: int = 64) -> str:
    """Generate a cryptographically random code verifier.

    The verifier must be 43–128 characters of URL-safe random data.
    In production, use os.urandom and encode as base64url.
    We use a simpler approach here since we are not cryptographically
    concerned in a simulation.
    """
    raw = os.urandom(length)
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")[:length]


def compute_code_challenge(verifier: str) -> str:
    """Compute SHA-256 hash of the verifier, base64url-encoded (no padding).

    This is the S256 method from RFC 7636.  The 'plain' method (sending the
    verifier as the challenge) is allowed by the spec but provides no
    additional security and should not be used.
    """
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def verify_challenge(verifier: str, stored_challenge: str) -> bool:
    """Verify that the verifier matches the stored challenge."""
    return compute_code_challenge(verifier) == stored_challenge
# mccole:/pkce_helpers


# mccole:pkce_client
class PKCEClient(Process):
    """OAuth client that uses PKCE for the authorization code flow.

    This client generates a code verifier before requesting authorization,
    sends the code challenge with the authorization request,
    and proves knowledge of the verifier when exchanging the code for a token.
    """

    def init(
        self,
        client_id: str,
        redirect_uri: str,
        auth_server_auth_queue: Queue,
        auth_server_token_queue: Queue,
    ) -> None:
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_server_auth_queue = auth_server_auth_queue
        self.auth_server_token_queue = auth_server_token_queue

        # PKCE clients have no client_secret (they are public clients).
        self.access_token: Optional[str] = None
        self._code_verifier: Optional[str] = None

        print(f"[{self.now:.1f}] PKCEClient '{client_id}' started (no client secret)")

    async def run(self) -> None:
        """Demonstrate the PKCE flow."""
        scopes = ["profile", "photos"]

        # Step 1: Generate verifier and challenge BEFORE the authorization request.
        self._code_verifier = generate_code_verifier()
        challenge = compute_code_challenge(self._code_verifier)
        print(
            f"[{self.now:.1f}] PKCEClient: Generated code verifier "
            f"(challenge={challenge[:12]}...)"
        )

        # Step 2: Send authorization request with the challenge.
        code = await self._request_authorization(scopes, challenge)
        if code is None:
            print(f"[{self.now:.1f}] PKCEClient: Authorization failed")
            return

        # Step 3: Exchange code for token using the verifier.
        token = await self._exchange_code(code)
        if token is None:
            print(f"[{self.now:.1f}] PKCEClient: Token exchange failed")
            return

        self.access_token = token
        print(f"[{self.now:.1f}] PKCEClient: Token acquired successfully via PKCE")

    async def _request_authorization(
        self, scopes: list[str], challenge: str
    ) -> Optional[str]:
        """Send authorization request including the code challenge."""
        from oauth_types import AuthorizationRequest

        state = generate_token("state")
        response_queue: Queue = Queue(self._env)

        # In a real request this would be an HTTP redirect to the authorization
        # server with code_challenge and code_challenge_method=S256 as query params.
        request = AuthorizationRequest(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=scopes,
            state=state,
            response_queue=response_queue,
        )
        # Attach PKCE fields (would be query parameters in real HTTP).
        request.code_challenge = challenge          # type: ignore[attr-defined]
        request.code_challenge_method = "S256"      # type: ignore[attr-defined]

        await self.auth_server_auth_queue.put(request)
        response = await response_queue.get()

        if response.state != state:
            print(f"[{self.now:.1f}] PKCEClient: State mismatch — CSRF?")
            return None

        return response.code

    async def _exchange_code(self, code: str) -> Optional[str]:
        """Exchange the authorization code for a token, proving the verifier."""
        from oauth_types import TokenRequest

        response_queue: Queue = Queue(self._env)

        request = TokenRequest(
            code=code,
            client_id=self.client_id,
            client_secret="",        # Public clients have no secret.
            redirect_uri=self.redirect_uri,
            response_queue=response_queue,
        )
        # Attach the code verifier — the server will hash it and compare.
        request.code_verifier = self._code_verifier   # type: ignore[attr-defined]

        await self.auth_server_token_queue.put(request)
        response: TokenResponse = await response_queue.get()

        if response.token_type == "error":
            print(f"[{self.now:.1f}] PKCEClient: Token exchange error")
            return None

        return response.access_token
# mccole:/pkce_client
