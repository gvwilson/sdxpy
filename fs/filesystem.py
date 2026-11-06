import struct

from disk import Disk

# mccole:constants
BLOCK_SIZE = 32
NUM_BLOCKS = 64
DISK_SIZE = BLOCK_SIZE * NUM_BLOCKS

INODE_SIZE = BLOCK_SIZE
NUM_INODES = 16

SUPERBLOCK_BLOCK = 0
INODE_TABLE_START = 1
DATA_START = INODE_TABLE_START + NUM_INODES

MAX_FILE_BLOCKS = 6
NAME_LEN = 12

MAGIC = 0x53504653  # the ASCII bytes "SPFS"

SUPERBLOCK = struct.Struct(">IIII")
INODE = struct.Struct(">IIIIIIII")
DIR_ENTRY = struct.Struct(">12sI")

KIND_FREE = 0
KIND_FILE = 1
KIND_DIR = 2

ROOT_INODE = 0
# mccole:/constants


class FileSystem:
    def __init__(self, disk=None):
        self.disk = disk if disk is not None else Disk(BLOCK_SIZE, NUM_BLOCKS)
        self.bitmap = bytearray(NUM_BLOCKS)

    # mccole:format
    def format(self):
        """Initialize the disk to hold an empty filesystem."""
        self.bitmap[:] = b"\x00" * NUM_BLOCKS
        for block in range(SUPERBLOCK_BLOCK, DATA_START):
            self.bitmap[block] = 1

        packed = SUPERBLOCK.pack(MAGIC, BLOCK_SIZE, NUM_BLOCKS, NUM_INODES)
        self.disk.write_block(SUPERBLOCK_BLOCK, packed)

        empty = INODE.pack(0, KIND_FREE, *([0] * MAX_FILE_BLOCKS))
        for i in range(NUM_INODES):
            self.disk.write_block(INODE_TABLE_START + i, empty)

        self._write_inode(ROOT_INODE, 0, KIND_DIR, [0] * MAX_FILE_BLOCKS)
    # mccole:/format

    # mccole:inode
    def _read_inode(self, inode_number):
        self._check_inode(inode_number)
        raw = self.disk.read_block(INODE_TABLE_START + inode_number)
        size, kind, *blocks = INODE.unpack(raw)
        return {"size": size, "kind": kind, "blocks": blocks}

    def _write_inode(self, inode_number, size, kind, blocks):
        self._check_inode(inode_number)
        raw = INODE.pack(size, kind, *blocks)
        self.disk.write_block(INODE_TABLE_START + inode_number, raw)

    def _check_inode(self, inode_number):
        if not (0 <= inode_number < NUM_INODES):
            raise ValueError(f"inode number {inode_number} out of range")
    # mccole:/inode

    # mccole:allocate
    def _allocate_block(self):
        for block in range(DATA_START, NUM_BLOCKS):
            if self.bitmap[block] == 0:
                self.bitmap[block] = 1
                return block
        raise OSError("disk is full")

    def _free_block(self, block):
        self.bitmap[block] = 0

    def _allocate_inode(self, kind):
        for i in range(NUM_INODES):
            if self._read_inode(i)["kind"] == KIND_FREE:
                self._write_inode(i, 0, kind, [0] * MAX_FILE_BLOCKS)
                return i
        raise OSError("no free inodes")
    # mccole:/allocate

    # mccole:data
    def _read_data(self, inode_number):
        inode = self._read_inode(inode_number)
        chunks = []
        for block in inode["blocks"]:
            if block == 0:
                break
            chunks.append(self.disk.read_block(block))
        return b"".join(chunks)[: inode["size"]]

    def _write_data(self, inode_number, data):
        inode = self._read_inode(inode_number)
        for block in inode["blocks"]:
            if block != 0:
                self._free_block(block)

        blocks = []
        for offset in range(0, len(data), BLOCK_SIZE):
            block = self._allocate_block()
            self.disk.write_block(block, data[offset : offset + BLOCK_SIZE])
            blocks.append(block)
        blocks += [0] * (MAX_FILE_BLOCKS - len(blocks))

        self._write_inode(inode_number, len(data), inode["kind"], blocks)
    # mccole:/data

    # mccole:dirent
    def _pack_dir_entry(self, name, inode_number):
        name_bytes = name.encode("utf-8")
        if len(name_bytes) > NAME_LEN:
            raise ValueError(f"name too long: {name}")
        return DIR_ENTRY.pack(name_bytes, inode_number)

    def _unpack_dir_entry(self, raw):
        name_bytes, inode_number = DIR_ENTRY.unpack(raw)
        name = name_bytes.split(b"\x00")[0].decode("utf-8")
        return name, inode_number

    def _list_dir(self, inode_number):
        data = self._read_data(inode_number)
        entries = []
        for offset in range(0, len(data), DIR_ENTRY.size):
            name, child = self._unpack_dir_entry(
                data[offset : offset + DIR_ENTRY.size]
            )
            entries.append((name, child))
        return entries

    def _dir_add(self, dir_inode, name, child_inode):
        data = self._read_data(dir_inode)
        raw = self._pack_dir_entry(name, child_inode)
        self._write_data(dir_inode, data + raw)

    def _dir_remove(self, dir_inode, name):
        kept = [
            self._pack_dir_entry(n, child)
            for (n, child) in self._list_dir(dir_inode)
            if n != name
        ]
        self._write_data(dir_inode, b"".join(kept))
    # mccole:/dirent

    # mccole:lookup
    def _split(self, path):
        if not path.startswith("/"):
            raise ValueError("absolute path required")
        if path == "/":
            raise ValueError("the root directory cannot be split")
        parent, _, name = path.rpartition("/")
        return (parent if parent != "" else "/"), name

    def _lookup(self, path):
        current = ROOT_INODE
        for name in [p for p in path.split("/") if p]:
            child = None
            for (entry_name, child_inode) in self._list_dir(current):
                if entry_name == name:
                    child = child_inode
                    break
            if child is None:
                return None
            current = child
        return current
    # mccole:/lookup

    # mccole:api
    def create(self, path):
        parent, name = self._split(path)
        parent_inode = self._lookup(parent)
        inode = self._allocate_inode(KIND_FILE)
        self._dir_add(parent_inode, name, inode)
        return inode

    def mkdir(self, path):
        parent, name = self._split(path)
        parent_inode = self._lookup(parent)
        inode = self._allocate_inode(KIND_DIR)
        self._dir_add(parent_inode, name, inode)

    def read(self, path):
        inode = self._lookup(path)
        if inode is None:
            raise FileNotFoundError(path)
        return self._read_data(inode)

    def write(self, path, data):
        inode = self._lookup(path)
        if inode is None:
            inode = self.create(path)
        self._write_data(inode, data)

    def listdir(self, path):
        inode = self._lookup(path)
        if inode is None:
            raise FileNotFoundError(path)
        return [name for (name, child) in self._list_dir(inode)]

    def remove(self, path):
        parent, name = self._split(path)
        parent_inode = self._lookup(parent)
        inode = self._lookup(path)
        if inode is None:
            raise FileNotFoundError(path)
        info = self._read_inode(inode)
        for block in info["blocks"]:
            if block != 0:
                self._free_block(block)
        self._write_inode(inode, 0, KIND_FREE, [0] * MAX_FILE_BLOCKS)
        self._dir_remove(parent_inode, name)
    # mccole:/api


# mccole:main
def main():
    fs = FileSystem()
    fs.format()
    fs.mkdir("/docs")
    fs.write("/docs/hello.txt", b"Hello, filesystem!\n")
    fs.write("/readme.txt", b"Read me first.\n")
    print("/ contains:", sorted(fs.listdir("/")))
    print("/docs contains:", sorted(fs.listdir("/docs")))
    print("/docs/hello.txt:", fs.read("/docs/hello.txt").decode().strip())
    fs.remove("/readme.txt")
    print("/ after removing /readme.txt:", sorted(fs.listdir("/")))


if __name__ == "__main__":
    main()
# mccole:/main
