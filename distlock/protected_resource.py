from asimpy import Environment


# mccole:protectedresource
class ProtectedResource:
    """A resource that validates fencing tokens."""

    def __init__(self, env: Environment, name: str):
        self.env = env
        self.name = name
        self.highest_token_seen = 0
        self.current_accessor: str | None = None

    async def access(self, client_id: str, token: int, duration: float):
        """Access the resource with a fencing token."""
        if token <= self.highest_token_seen:
            print(
                f"[{self.env.now:.1f}] FENCING: {self.name} rejected "
                f"{client_id} (stale token {token}, seen {self.highest_token_seen})"
            )
            return False

        self.highest_token_seen = token
        self.current_accessor = client_id

        print(
            f"[{self.env.now:.1f}] {self.name}: {client_id} accessing (token {token})"
        )

        await self.env.timeout(duration)

        print(f"[{self.env.now:.1f}] {self.name}: {client_id} finished")
        self.current_accessor = None
        return True
# mccole:/protectedresource
