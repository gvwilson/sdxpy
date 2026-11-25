"""Basic BitTorrent protocol demonstration."""

from asimpy import Environment
from typing import List
from tracker import Tracker
from simplified_peer import SimplifiedPeer
from bittorrent_types import TorrentMetadata


# mccole:basicexample
def run_basic_bittorrent() -> None:
    """Demonstrate basic BitTorrent operation."""
    env = Environment()

    # Create tracker
    tracker = Tracker(env)

    # Create torrent metadata
    metadata = TorrentMetadata(
        info_hash="abc123",
        piece_length=256 * 1024,  # 256 KB pieces
        total_pieces=10,
        piece_hashes=["hash" + str(i) for i in range(10)],
        file_name="example.iso",
        file_size=10 * 256 * 1024,
        tracker_url="http://tracker.example.com:8080/announce",
    )

    print(f"[{env.now:.1f}] Created {metadata}\n")

    # Create initial seeder with all pieces
    peers: List[SimplifiedPeer] = []
    seeder = SimplifiedPeer(
        env,
        "Seeder",
        metadata,
        tracker,
        peers,
        initial_pieces=list(range(10)),  # Has all pieces
    )
    peers.append(seeder)

    # Create leechers with no pieces
    for i in range(3):
        peer = SimplifiedPeer(
            env, f"Peer{i + 1}", metadata, tracker, peers, initial_pieces=[]
        )
        peers.append(peer)

    # Update peer lists
    for peer in peers:
        peer.other_peers = [p for p in peers if p != peer]

    # Run simulation
    env.run(until=30)

    # Print statistics
    print(f"\n{'=' * 60}")
    print("Final Statistics:")
    print("=" * 60)
    for peer in peers:
        print(
            f"{peer.peer_id}: Downloaded={peer.downloaded_pieces}, "
            f"Uploaded={peer.uploaded_pieces}"
        )
# mccole:/basicexample


if __name__ == "__main__":
    run_basic_bittorrent()
