---
title: "A Simple Filesystem"
version: 2
abstract: >
    Every program reads and writes files, but very few programmers know
    what happens between opening a file and reading from it.
    This chapter builds a small filesystem on top of an in-memory array of bytes
    to show how disks, blocks, inodes, and directories fit together.
syllabus:
-   A disk is just a sequence of bytes, but filesystems read and write it in fixed-size blocks.
-   A superblock holds the metadata needed to interpret everything else on the disk.
-   A bitmap records which blocks are in use and which are free.
-   An inode stores a file's metadata and the numbers of the blocks holding its contents.
-   A directory is a file whose contents map names to inode numbers.
-   Paths are resolved by walking from the root directory down to the target entry.
depends:
-   binary
-   persist
---

Every program reads and writes files,
but few of us ever stop to ask what happens in between.
When we open a file and then read from it,
some piece of software has to figure out where our data lives on a disk,
find the bytes,
and hand them back to us.
This chapter builds a tiny filesystem
to show how that piece of software works.

We will not touch a real disk.
Instead,
we will use an in-memory array of bytes to *simulate* one.
As [%x binary %] explains,
bytes are just numbers,
so a `bytearray` in Python is a perfectly good stand-in
for the raw storage of a physical device.
The ideas we build here—blocks, superblocks, inodes, directories—are
the same ones used by real filesystems such as ext4 and NTFS.

## A Disk of Bytes {: #fs-disk}

A physical disk stores a long sequence of bytes,
but reading and writing them one at a time would be painfully slow.
Real filesystems therefore group bytes into [%i "block" %]s of a fixed size
and always read or write whole blocks at once.
Our simulated disk does the same thing:

[%inc disk.py mark=class %]

A `Disk` is just a `bytearray` of `block_size * block_count` bytes.
`read_block` returns one block's worth of bytes,
and `write_block` overwrites a block,
padding with zero bytes if the data we supply is shorter than a block.
The `_check_block` method ensures that
block numbers are in the range `0` to `block_count - 1`.

<div class="callout" markdown="1">

### Why Fixed-Size Blocks?

Grouping bytes into blocks trades a little wasted space for simplicity and speed.
If every block is the same size,
we can find block $N$ by multiplying instead of searching:
it always starts at byte $N \times B$,
where $B$ is the block size.
The wasted space comes from files that don't fill their last block,
but the trade is almost always worthwhile.

</div>

## The Superblock {: #fs-super}

The first thing our filesystem needs is a way to recognize itself.
If we are handed a `bytearray` full of bytes,
how do we know whether it is one of *our* filesystems
or just random garbage?
The answer is to store some [%g metadata "metadata" %] in the first block:

[%inc filesystem.py mark=constants %]

The constant `MAGIC` is a number chosen so that
when it is packed into four bytes it spells `"SPFS"`.
`struct.Struct` describes how to pack and unpack values;
the format string `">IIII"` means "four unsigned 32-bit integers in big-endian order",
a topic we first met in [%x binary %].
Our superblock therefore records:

- the magic number used to identify the filesystem;

- the block size and the number of blocks;

- the number of inodes (which we will meet shortly).

The `format` method writes a fresh superblock
and initializes everything else:

[%inc filesystem.py mark=format %]

Formatting first clears the [%i "bitmap" %] (which we discuss next)
and marks the blocks that hold the superblock and the inode table as being in use.
It then writes the superblock into block 0,
fills every inode with zeros to mark it as free,
and creates the root directory in inode 0.

## Free Blocks {: #fs-free}

A filesystem must remember which blocks are occupied and which are available.
The simplest way to do this is a bitmap:
an array with one entry per block
that is `1` if the block is in use and `0` if it is free.

[%inc filesystem.py mark=allocate %]

`_allocate_block` scans the bitmap for the first free block.
`_free_block` simply marks a block as free again.
`_allocate_inode` does the same job for inodes:
it finds an inode whose kind is `KIND_FREE`
and initializes it.

<div class="callout" markdown="1">

### In Memory, Not on Disk

We keep the bitmap in a Python `bytearray` inside the `FileSystem` object.
A real filesystem would store its bitmap in a reserved region of the disk
so that it survives a restart.
Turning our in-memory bitmap into an on-disk one is a good exercise.

</div>

## Inodes and Files {: #fs-inode}

A file is more than its contents.
It also has a size,
a kind (file or directory),
and—crucially—a list of the blocks that hold its data.
We store this [%g metadata "metadata" %] in a structure called an [%i "inode" %]:

[%inc filesystem.py mark=inode %]

Each inode is exactly `INODE_SIZE` bytes long,
and because `INODE_SIZE` equals `BLOCK_SIZE`,
one inode fits in one block.
Inode $i$ therefore lives in block `INODE_TABLE_START + i`.
The inode stores the file's size,
its kind,
and up to `MAX_FILE_BLOCKS` block numbers.

Reading and writing a file's contents
means following those block numbers:

[%inc filesystem.py mark=data %]

`_read_data` reads each block listed in the inode,
joins them together,
and trims the result to the file's recorded size.
`_write_data` does the reverse:
it frees the file's old blocks,
allocates fresh ones,
and copies the data into them one block at a time.

This indirection—storing *pointers to* data rather than the data itself—is
the heart of how filesystems work.
The inode is small and fixed in size,
but the file it describes can be larger
and scattered across the disk.

## Directories {: #fs-dir}

If a file is "a list of blocks",
then a [%i "directory" %] is "a file whose contents are a list of names".
Each directory entry maps a name to an inode number:

[%inc filesystem.py mark=dirent %]

A directory entry is 16 bytes:
12 for the name (padded with zero bytes if it is shorter)
and 4 for the inode number.
`_list_dir` reads the directory's data
and unpacks it into a list of `(name, inode)` pairs.
`_dir_add` and `_dir_remove` add and remove entries
by rewriting the directory's contents.

Notice that we never check that a directory entry is "really" a directory:
to the filesystem, a directory is just a file with a particular structure.
This is a small example of a larger design idea
that we first met in [%x persist %]:
a program is just another kind of data.

## Paths and Operations {: #fs-path}

The last piece of the puzzle is turning a path like `/docs/hello.txt`
into the file it names.
We do this by walking from the root directory
down through each component of the path:

[%inc filesystem.py mark=lookup %]

`_lookup` starts at `ROOT_INODE` and, for each name in the path,
looks it up in the current directory.
If any component is missing, it returns `None`.
`_split` separates a path into its parent directory and final name.

The public methods are then straightforward compositions
of the pieces we have already built:

[%inc filesystem.py mark=api %]

`create` and `mkdir` allocate an inode and add an entry to the parent directory.
`write` creates the file if it doesn't exist and then stores the data.
`read`, `listdir`, and `remove` look up an inode and act on it.
None of these methods is more than a few lines long
because each one is standing on the shoulders of the ones below it.

## Testing {: #fs-test}

As in earlier chapters,
we test our code with small examples rather than a real disk:

[%inc test_disk.py mark=sample %]

and:

[%inc test_filesystem.py mark=make %]

[%inc test_filesystem.py mark=sample %]

The tests create a filesystem in memory,
format it,
and then check that files can be created, read, overwritten, and removed.
Because our "disk" is just a `bytearray`,
each test runs in a few microseconds
and needs no cleanup afterward.

## Summary {: #fs-summary}

Filesystems look complicated,
but they are built from a small number of simple ideas stacked on top of each other.
A disk is a sequence of bytes grouped into blocks.
A superblock records how to interpret those blocks.
A bitmap tracks which blocks are free.
Inodes hold a file's metadata and point to its data.
Directories are files that map names to inodes.
And paths are just walks from the root directory down to a particular entry.

<section class="exercises" markdown="1">
## Exercises {: #fs-exercises}

### Delete a Directory

Modify `remove` so that it can delete a directory
by recursively deleting everything inside it first.
How do you prevent the user from accidentally deleting the root directory?

### Persist the Bitmap

Store the block bitmap in a reserved block on the disk
instead of keeping it in memory,
and update `format` and the allocation methods to use it.

### Longer Files

Our inodes support at most `MAX_FILE_BLOCKS` data blocks.
Add a single [%i "indirect block" %]
that stores the numbers of additional data blocks
so that a file can grow much larger.

### Variable-Length Names

Replace the fixed 12-byte name field in a directory entry
with a length prefix and a variable-length name.
What are the trade-offs between the two designs?

### Hard Links

Add a `link` operation that creates a second name for an existing inode,
and modify `remove` so that an inode is freed only when its last name is removed.
What does this imply about where the file's size is stored?

### Detect a Foreign Disk

Modify the constructor so that it refuses to work
with a `Disk` whose magic number doesn't match.
What should happen if the magic number is missing but the disk is otherwise valid?

</section>
