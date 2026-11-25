"""BitTorrent tracker implementation."""

from asimpy import Process, Queue
from typing import Dict, Set
from bittorrent_types import TrackerRequest, TrackerResponse, PeerInfo
import random


# mccole:tracker_init
class Tracker(Process):
    """BitTorrent tracker coordinating peers."""

    def init(self) -> None:
        self.request_queue: Queue = Queue(self._env)

        # Track peers for each torrent (by info_hash)
        self.swarms: Dict[str, Set[PeerInfo]] = {}

        # Track when peers were last seen
        self.peer_last_seen: Dict[str, float] = {}

        print(f"[{self.now:.1f}] Tracker started")

    async def run(self) -> None:
        """Main tracker loop."""
        while True:
            request = await self.request_queue.get()
            await self.handle_request(request)
    # mccole:/tracker_init

    # mccole:tracker_handle
    async def handle_request(self, request: TrackerRequest) -> None:
        """Handle tracker announce request."""
        print(f"[{self.now:.1f}] Tracker: Received {request}")

        # Initialize swarm if needed
        if request.info_hash not in self.swarms:
            self.swarms[request.info_hash] = set()

        swarm = self.swarms[request.info_hash]

        # Create peer info
        peer = PeerInfo(
            peer_id=request.peer_id, ip_address="127.0.0.1", port=request.port
        )

        # Handle different events
        if request.event == "started" or request.event == "":
            swarm.add(peer)
            self.peer_last_seen[request.peer_id] = self.now
            print(
                f"[{self.now:.1f}] Tracker: Added {peer.peer_id} to swarm "
                f"(total: {len(swarm)})"
            )

        elif request.event == "stopped":
            swarm.discard(peer)
            print(f"[{self.now:.1f}] Tracker: Removed {peer.peer_id} from swarm")

        elif request.event == "completed":
            self.peer_last_seen[request.peer_id] = self.now
            print(f"[{self.now:.1f}] Tracker: {peer.peer_id} completed download")

        # Return list of other peers
        other_peers = [p for p in swarm if p.peer_id != request.peer_id]

        # Limit to 50 peers (typical tracker behavior)
        if len(other_peers) > 50:
            other_peers = random.sample(other_peers, 50)

        response = TrackerResponse(
            interval=30,  # Re-announce every 30 seconds
            peers=other_peers,
        )

        await request.response_queue.put(response)

        print(
            f"[{self.now:.1f}] Tracker: Sent {len(other_peers)} peers to "
            f"{request.peer_id}"
        )
    # mccole:/tracker_handle
