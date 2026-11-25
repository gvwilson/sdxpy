"""Data types for BitTorrent protocol implementation."""

from dataclasses import dataclass
from typing import List, Any
from asimpy import Queue
import hashlib


# mccole:file_types
@dataclass
class Piece:
    """A piece of the file being shared."""

    index: int
    data: bytes
    hash_value: str  # SHA-1 hash for verification

    def verify(self) -> bool:
        """Verify piece integrity against hash."""
        computed_hash = hashlib.sha1(self.data).hexdigest()
        return computed_hash == self.hash_value


@dataclass
class TorrentMetadata:
    """Metadata from .torrent file."""

    info_hash: str  # Unique identifier for this torrent
    piece_length: int  # Size of each piece in bytes
    total_pieces: int  # Number of pieces
    piece_hashes: List[str]  # SHA-1 hash for each piece
    file_name: str
    file_size: int
    tracker_url: str

    def __str__(self) -> str:
        return f"Torrent({self.file_name}, {self.total_pieces} pieces)"


@dataclass
class PeerInfo:
    """Information about a peer."""

    peer_id: str
    ip_address: str
    port: int

    def __str__(self) -> str:
        return f"Peer({self.peer_id})"

    def __hash__(self) -> int:
        return hash(self.peer_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PeerInfo):
            return False
        return self.peer_id == other.peer_id
# mccole:/file_types


# mccole:message_types
@dataclass
class TrackerRequest:
    """Request to tracker."""

    info_hash: str
    peer_id: str
    port: int
    uploaded: int
    downloaded: int
    left: int  # Bytes remaining to download
    event: str  # "started", "completed", "stopped"
    response_queue: Queue

    def __str__(self) -> str:
        return f"TrackerReq(peer={self.peer_id}, event={self.event})"


@dataclass
class TrackerResponse:
    """Response from tracker."""

    interval: int  # Seconds until next tracker request
    peers: List[PeerInfo]

    def __str__(self) -> str:
        return f"TrackerResp({len(self.peers)} peers)"


@dataclass
class PeerMessage:
    """Message exchanged between peers."""

    msg_type: str  # "choke", "unchoke", "interested", "have", "request", "piece"
    payload: Any = None

    def __str__(self) -> str:
        if self.msg_type == "have":
            return f"Have(piece={self.payload})"
        elif self.msg_type == "request":
            return f"Request(piece={self.payload})"
        elif self.msg_type == "piece":
            piece_idx = self.payload.index if isinstance(self.payload, Piece) else "?"
            return f"Piece(index={piece_idx})"
        return f"Msg({self.msg_type})"


@dataclass
class BitfieldMessage:
    """Bitfield indicating which pieces a peer has."""

    bitfield: List[bool]  # True if peer has piece at that index

    def has_piece(self, index: int) -> bool:
        """Check if peer has a specific piece."""
        return index < len(self.bitfield) and self.bitfield[index]

    def __str__(self) -> str:
        count = sum(1 for b in self.bitfield if b)
        return f"Bitfield({count}/{len(self.bitfield)} pieces)"
# mccole:/message_types
