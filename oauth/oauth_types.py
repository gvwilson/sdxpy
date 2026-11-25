"""Data types for OAuth 2.0 implementation."""

from dataclasses import dataclass
from asimpy import Queue
from typing import Any
import random
import string


# mccole:token_func
def generate_token(prefix: str = "tok") -> str:
    """Generate a random token."""
    random_part = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"{prefix}_{random_part}"
# mccole:/token_func


# mccole:message_types
@dataclass
class AuthorizationRequest:
    """Request for user authorization."""

    client_id: str
    redirect_uri: str
    scope: list[str]
    state: str  # CSRF protection
    response_queue: Queue

    def __str__(self):
        return f"AuthRequest(client={self.client_id}, scope={self.scope})"


@dataclass
class AuthorizationResponse:
    """Response with authorization code."""

    code: str
    state: str

    def __str__(self):
        return f"AuthResponse(code={self.code[:8]}...)"


@dataclass
class TokenRequest:
    """Request to exchange code for access token."""

    code: str
    client_id: str
    client_secret: str
    redirect_uri: str
    response_queue: Queue

    def __str__(self):
        return f"TokenRequest(client={self.client_id})"


@dataclass
class TokenResponse:
    """Response with access token."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: str | None = None
    scope: list[str] | None = None

    def __str__(self):
        return f"TokenResponse(token={self.access_token[:8]}...)"


@dataclass
class ResourceRequest:
    """Request to access protected resource."""

    access_token: str
    resource_path: str
    response_queue: Queue

    def __str__(self):
        return f"ResourceRequest(path={self.resource_path})"


@dataclass
class ResourceResponse:
    """Response from resource server."""

    success: bool
    data: Any = None
    error: str | None = None

    def __str__(self):
        if self.success:
            return "ResourceResponse(success=True)"
        return f"ResourceResponse(error={self.error})"
# mccole:/message_types


# mccole:internal_types
@dataclass
class AuthorizationCode:
    """Authorization code with metadata."""

    code: str
    client_id: str
    redirect_uri: str
    scope: list[str]
    expires_at: float
    used: bool = False

    def is_valid(self, now: float) -> bool:
        """Check if code is still valid."""
        return not self.used and now < self.expires_at


@dataclass
class AccessToken:
    """Access token with metadata."""

    token: str
    client_id: str
    scope: list[str]
    expires_at: float

    def is_valid(self, now: float) -> bool:
        """Check if token is still valid."""
        return now < self.expires_at
# mccole:/internal_types


# mccole:refresh
@dataclass
class RefreshToken:
    """Refresh token for obtaining new access tokens."""

    token: str
    client_id: str
    scope: list[str]
    expires_at: float

    def is_valid(self, now: float) -> bool:
        return now < self.expires_at
# mccole:/refresh
