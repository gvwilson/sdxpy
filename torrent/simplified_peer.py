"""Simplified BitTorrent peer for simulation."""

from asimpy import Process
from typing import List, Set, Dict, Optional, TYPE_CHECKING
from bittorrent_types import TorrentMetadata
import random

if TYPE_CHECKING:
    from tracker import Tracker


# mccole:peer_init
class SimplifiedPeer(Process):
    """Simplified peer for simulation purposes."""

    def init(
        self,
        peer_id: str,
        metadata: TorrentMetadata,
        tracker: "Tracker",
        other_peers: List["SimplifiedPeer"],
        initial_pieces: Optional[List[int]] = None,
    ) -> None:
        self.peer_id = peer_id
        self.metadata = metadata
        self.tracker = tracker
        self.other_peers = other_peers

        # Which pieces we have (just indices for simplicity)
        self.have_pieces: Set[int] = set(initial_pieces) if initial_pieces else set()

        # Statistics
        self.downloaded_pieces = len(self.have_pieces)
        self.uploaded_pieces = 0

        print(
            f"[{self.now:.1f}] Peer {self.peer_id}: Started with "
            f"{len(self.have_pieces)}/{metadata.total_pieces} pieces"
        )

    def is_complete(self) -> bool:
        """Check if download is complete."""
        return len(self.have_pieces) == self.metadata.total_pieces
    # mccole:/peer_init

    # mccole:peer_run
    async def run(self) -> None:
        """Simplified download loop."""
        # Announce to tracker
        await self.announce("started")

        # Download pieces
        while not self.is_complete():
            await self.download_round()
            await self.timeout(1.0)

        print(f"[{self.now:.1f}] Peer {self.peer_id}: ✓ Download complete!")

        # Announce completion
        await self.announce("completed")

        # Continue seeding
        await self.timeout(3.0)

    async def announce(self, event: str) -> None:
        """Simplified tracker announce."""
        print(f"[{self.now:.1f}] Peer {self.peer_id}: Announcing '{event}' to tracker")
    # mccole:/peer_run

    # mccole:peer_download_round
    async def download_round(self) -> None:
        """Attempt to download pieces from peers."""
        needed = [
            i for i in range(self.metadata.total_pieces) if i not in self.have_pieces
        ]

        if not needed:
            return

        # Rarest first
        piece_counts: Dict[int, int] = {}
        for peer in self.other_peers:
            for piece_idx in peer.have_pieces:
                piece_counts[piece_idx] = piece_counts.get(piece_idx, 0) + 1

        needed.sort(key=lambda idx: piece_counts.get(idx, 0))

        # Try to download rarest piece we need
        for piece_idx in needed[:3]:
            # Find peer with this piece
            candidates = [p for p in self.other_peers if piece_idx in p.have_pieces]

            if candidates:
                peer = random.choice(candidates)
                await self.download_piece_from(peer, piece_idx)
                break
    # mccole:/peer_download_round

    # mccole:peer_download_from
    async def download_piece_from(self, peer: "SimplifiedPeer", piece_idx: int) -> None:
        """Download a piece from a peer."""
        # Simulate transfer time
        await self.timeout(0.2)

        self.have_pieces.add(piece_idx)
        self.downloaded_pieces += 1
        peer.uploaded_pieces += 1

        print(
            f"[{self.now:.1f}] Peer {self.peer_id}: Downloaded piece {piece_idx} "
            f"from {peer.peer_id} ({len(self.have_pieces)}/"
            f"{self.metadata.total_pieces})"
        )
    # mccole:/peer_download_from
