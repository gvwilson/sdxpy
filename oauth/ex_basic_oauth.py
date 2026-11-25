"""Basic OAuth 2.0 authorization code flow demonstration."""

from asimpy import Environment
from authorization_server import AuthorizationServer
from resource_server import ResourceServer
from oauth_client import OAuthClient
from dsdx import dsdx


# mccole:sim
def main():
    """Demonstrate basic OAuth 2.0 authorization code flow."""
    env = Environment()

    # Create authorization server
    auth_server = AuthorizationServer(env)

    # Create resource server
    resource_server = ResourceServer(env, auth_server)

    # Register client application
    client_id = "photo_app"
    client_secret = "secret_xyz"
    redirect_uri = "https://photoapp.example.com/callback"

    auth_server.register_client(
        client_id=client_id, client_secret=client_secret, redirect_uris=[redirect_uri]
    )

    # Create client
    OAuthClient(
        env,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        auth_server=auth_server,
        resource_server=resource_server,
    )

    # Run simulation
    env.run(until=20)
# mccole:/sim


if __name__ == "__main__":
    dsdx(main)
