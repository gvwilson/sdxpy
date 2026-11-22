---
title: "A Simple Filesystem"
---

<section class="slide" markdown="1">

## Overview

-   A filesystem turns a flat sequence of bytes into files and directories

-   We build one on top of an in-memory byte array

-   Key ideas: blocks, superblock, bitmap, inodes, directories, path resolution

</section>
<section class="slide" markdown="1">

## A Disk of Bytes

-   A disk is a sequence of bytes

-   Group them into fixed-size blocks

-   `Disk` wraps a `bytearray` with `read_block` and `write_block`

</section>
<section class="slide" markdown="1">

## Superblock and Bitmap

-   Block 0 holds metadata: magic number, sizes, counts

-   A bitmap records which blocks are in use

-   `format` initializes the whole disk

</section>
<section class="slide" markdown="1">

## Inodes and Directories

-   An inode holds a file's size, kind, and block numbers

-   Indirection lets a small inode describe a larger file

-   A directory is a file whose contents map names to inodes

</section>
<section class="slide" markdown="1">

## Putting It Together

-   Paths are walks from the root down to a target

-   `create`, `write`, `read`, `mkdir`, `listdir`, `remove`

</section>
