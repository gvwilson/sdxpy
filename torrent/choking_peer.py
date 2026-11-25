"""BitTorrent peer with choking/unchoking algorithm and piece verification.

This module implements two features that the simplified peer omits:

1. Choking algorithm:
   Each peer maintains "slots" for the peers it uploads to.
   It prefers to upload to peers that upload back (tit-for-tat),
   keeping its top 4 uploaders unchoked.
   Every 30 seconds it also "optimistically unchokes" one random choked peer,
   giving new peers a chance to prove themselves.

2. Piece verification:
   After downloading a piece, the peer checks its SHA-1 hash against
   the expected hash in the torrent metadata.
   A corrupted or malicious piece is discarded and re-requested.
   This is what the `piece_hashes` field in `TorrentMetadata` is for.
"""

import random
import hashlib
from dataclasses import dataclass, field
from asimpy import Process
from typing import Dict, List, Set, Optional, TYPE_CHECKING
from bittorrent_types import TorrentMetadata, Piece

if TYPE_CHECKING:
    from simplified_peer import SimplifiedPeer

# Number of upload slots before the optimistic slot.
MAX_UNCHOKED = 4
# How often to re-evaluate who to unchoke (simulated seconds).
UNCHOKE_INTERVAL = 3.0
# How often to do an optimistic unchoke rotation.
OPTIMISTIC_INTERVAL = 9.0


# mccole:upload_record
@dataclass
class UploadRecord:
    """Tracks how much a peer has uploaded to us in the recent window."""

    peer_id: str
    bytes_received: int = 0   # bytes downloaded FROM this peer recently
    is_choked: bool = True    # are we choking this peer (refusing to upload)?
# mccole:/upload_record


# mccole:choking_peer
class ChokingPeer(Process):
    """Peer with a proper choking algorithm and piece verification.

    Hidden complexity:
    The real BitTorrent choking algorithm measures upload rate over a 20-second
    rolling window, not total bytes.  Peers that have good upload rates *recently*
    are unchoked; peers whose rates drop are re-choked.  This prevents a peer that
    uploaded a lot in the past but is now idle from monopolizing upload slots.
    We use a simpler sliding counter here; the structure is the same.
    """

    def init(
        self,
        peer_id: str,
        metadata: TorrentMetadata,
        other_peers: List["SimplifiedPeer"],
        initial_pieces: Optional[List[int]] = None,
    ) -> None:
        self.peer_id = peer_id
        self.metadata = metadata
        self.other_peers = other_peers

        self.have_pieces: Set[int] = set(initial_pieces or [])
        self.upload_records: Dict[str, UploadRecord] = {}
        self.optimistic_peer: Optional[str] = None

        # Statistics
        self.downloaded_pieces = len(self.have_pieces)
        self.uploaded_pieces = 0
        self.rejected_pieces = 0   # failed hash verification

        for peer in other_peers:
            self.upload_records[peer.peer_id] = UploadRecord(peer_id=peer.peer_id)

        print(
            f"[{self.now:.1f}] Peer {self.peer_id}: Started with "
            f"{len(self.have_pieces)}/{metadata.total_pieces} pieces"
        )

    def is_complete(self) -> bool:
        return len(self.have_pieces) == self.metadata.total_pieces

    async def run(self) -> None:
        """Download loop with concurrent unchoke timer."""
        _UnchokeTimer(self._env, self)
        _OptimisticUnchokeTimer(self._env, self)

        while not self.is_complete():
            await self._download_round()
            await self.timeout(1.0)

        print(f"[{self.now:.1f}] Peer {self.peer_id}: Download complete!")
    # mccole:/choking_peer

    # mccole:unchoke_logic
    def rechoke(self) -> None:
        """Re-evaluate which peers to unchoke based on upload rate.

        The top MAX_UNCHOKED peers by bytes_received are unchoked.
        All others are choked (unless they are the current optimistic unchoke).
        After evaluating, reset the counters for the next interval.
        """
        records = list(self.upload_records.values())
        records.sort(key=lambda r: r.bytes_received, reverse=True)

        for i, record in enumerate(records):
            if record.peer_id == self.optimistic_peer:
                record.is_choked = False   # Always unchoke the optimistic slot.
            else:
                record.is_choked = i >= MAX_UNCHOKED

        print(
            f"[{self.now:.1f}] Peer {self.peer_id}: Rechoked. "
            f"Unchoked: {[r.peer_id for r in records if not r.is_choked]}"
        )

        # Reset counters for next interval.
        for record in records:
            record.bytes_received = 0

    def rotate_optimistic(self) -> None:
        """Rotate the optimistic unchoke to a randomly-chosen choked peer.

        This gives new or slow peers a chance to prove they can upload.
        Without optimistic unchoking, a peer that joined the swarm after the
        top uploaders were established would never get unchoked and could
        never start downloading.
        """
        choked = [r.peer_id for r in self.upload_records.values() if r.is_choked]
        if choked:
            self.optimistic_peer = random.choice(choked)
            if self.optimistic_peer in self.upload_records:
                self.upload_records[self.optimistic_peer].is_choked = False
            print(
                f"[{self.now:.1f}] Peer {self.peer_id}: "
                f"Optimistically unchoked {self.optimistic_peer}"
            )
    # mccole:/unchoke_logic

    # mccole:piece_verification
    async def _download_round(self) -> None:
        """Download one piece using rarest-first selection."""
        needed = [
            i for i in range(self.metadata.total_pieces) if i not in self.have_pieces
        ]
        if not needed:
            return

        # Rarest-first: count how many peers have each piece.
        piece_counts: Dict[int, int] = {}
        for peer in self.other_peers:
            for idx in peer.have_pieces:
                piece_counts[idx] = piece_counts.get(idx, 0) + 1

        needed.sort(key=lambda idx: piece_counts.get(idx, 0))

        for piece_idx in needed[:3]:
            candidates = [
                p for p in self.other_peers
                if piece_idx in p.have_pieces
                and self.upload_records.get(p.peer_id, UploadRecord(p.peer_id)).is_choked is False
            ]
            if not candidates:
                # No unchoked peer has this piece; try any peer.
                candidates = [
                    p for p in self.other_peers if piece_idx in p.have_pieces
                ]
            if candidates:
                source = random.choice(candidates)
                await self._download_and_verify(source, piece_idx)
                # Record that this peer uploaded to us.
                if source.peer_id in self.upload_records:
                    self.upload_records[source.peer_id].bytes_received += 1
                source.uploaded_pieces += 1
                break

    async def _download_and_verify(
        self, source: "SimplifiedPeer", piece_idx: int
    ) -> None:
        """Download a piece and verify its SHA-1 hash.

        If verification fails the piece is discarded.
        In real BitTorrent, a peer that repeatedly sends bad pieces is banned.
        """
        await self.timeout(0.2)   # simulate transfer time

        # Simulate the piece data (in a real system this would be actual bytes).
        fake_data = f"piece-{piece_idx}-from-{source.peer_id}".encode()
        expected_hash = self.metadata.piece_hashes[piece_idx]
        actual_hash = hashlib.sha1(fake_data).hexdigest()

        if actual_hash == expected_hash:
            self.have_pieces.add(piece_idx)
            self.downloaded_pieces += 1
            print(
                f"[{self.now:.1f}] Peer {self.peer_id}: "
                f"Verified piece {piece_idx} from {source.peer_id} "
                f"({len(self.have_pieces)}/{self.metadata.total_pieces})"
            )
        else:
            # Hash mismatch — corrupt or tampered piece.
            self.rejected_pieces += 1
            print(
                f"[{self.now:.1f}] Peer {self.peer_id}: "
                f"REJECTED piece {piece_idx} from {source.peer_id} "
                f"(hash mismatch)"
            )
    # mccole:/piece_verification


class _UnchokeTimer(Process):
    """Periodically calls `rechoke` on the owning peer."""

    def init(self, peer: ChokingPeer) -> None:
        self.peer = peer

    async def run(self) -> None:
        while True:
            await self.timeout(UNCHOKE_INTERVAL)
            self.peer.rechoke()


class _OptimisticUnchokeTimer(Process):
    """Periodically rotates the optimistic unchoke slot."""

    def init(self, peer: ChokingPeer) -> None:
        self.peer = peer

    async def run(self) -> None:
        while True:
            await self.timeout(OPTIMISTIC_INTERVAL)
            self.peer.rotate_optimistic()
