# mccole:class
class Disk:
    """A fixed-size array of bytes divided into fixed-size blocks."""

    def __init__(self, block_size, block_count):
        self.block_size = block_size
        self.block_count = block_count
        self._data = bytearray(block_size * block_count)

    @property
    def size(self):
        """The total number of bytes on the disk."""
        return len(self._data)

    def read_block(self, block_number):
        """Return the contents of a block as a ``bytes`` object."""
        self._check_block(block_number)
        start = block_number * self.block_size
        return bytes(self._data[start : start + self.block_size])

    def write_block(self, block_number, data):
        """Overwrite a block with ``data``, padding with zero bytes as needed."""
        self._check_block(block_number)
        if len(data) > self.block_size:
            raise ValueError("data does not fit in a single block")
        start = block_number * self.block_size
        self._data[start : start + self.block_size] = b"\x00" * self.block_size
        self._data[start : start + len(data)] = data

    def _check_block(self, block_number):
        if not (0 <= block_number < self.block_count):
            raise ValueError(f"block number {block_number} out of range")
# mccole:/class
