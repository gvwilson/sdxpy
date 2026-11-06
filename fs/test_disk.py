from disk import Disk

# mccole:sample
def test_write_block_pads_with_zeros():
    disk = Disk(block_size=16, block_count=4)
    disk.write_block(0, b"hello")
    assert disk.read_block(0) == b"hello" + b"\x00" * 11
# mccole:/sample


def test_write_block_rejects_oversized_data():
    disk = Disk(block_size=4, block_count=2)
    try:
        disk.write_block(0, b"hello")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_block_number_out_of_range():
    disk = Disk(block_size=16, block_count=4)
    try:
        disk.read_block(4)
        assert False, "expected ValueError"
    except ValueError:
        pass
