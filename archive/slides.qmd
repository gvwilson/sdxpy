---
title: "A File Archiver"
---

<section class="slide" markdown="1">

## The Problem

-   Want to save snapshots of work in progress

-   Create a simple [%g version_control_system "version control system" %]

-   And show how to test it using mock objects ([%x protocols %])

</section>
<section class="slide" markdown="1">

## Design

-   Wasteful to store the same file repeatedly

-   So if the file's hash is `abcd1234`, save it as `abcd1234.bck`

    -   Handles renaming

-   Then create a [%g manifest "manifest" %] to show
    what unique blocks of bytes had what names when

</section>
<section class="slide" markdown="1">

## Storage

[% figure
   slug="archive-storage"
   img="storage.svg"
   alt="Backup file storage"
   caption="Organization of backup file storage."
%]

</section>
<section class="slide" markdown="1">

## Finding and Hashing

-   Use globbing ([%x glob %]) and hashing ([%x dup %])

[%inc hash_all.py mark=func %]

</section>
<section class="slide" markdown="1">

## Finding and Hashing

[%inc sample_dir.out %]
[%inc hash_all.sh %]
[%inc hash_all.out %]

</section>
<section class="slide" markdown="1">

## Testing

-   Obvious approach is to create lots of files and directories

-   But we want to test what happens when they change,
    which makes things complicated to maintain

-   Use a [%g mock_object "mock object" %] ([%x protocols %])
    instead of the real filesystem

</section>
<section class="slide" markdown="1">

## Faking the Filesystem

-   [pyfakefs][pyfakefs] replaces functions like `open`
    with ones that behave the same way
    but act on "files" stored in memory

[% figure
   slug="archive-mock-fs"
   img="mock_fs.svg"
   alt="Mock filesystem"
   caption="Using a mock filesystem to simplify testing."
%]

-   `import pyfakefs` automatically creates a fixture called `fs`

</section>
<section class="slide" markdown="1">

## Direct Use

[%inc test_mock_fs.py %]

</section>
<section class="slide" markdown="1">

## Build Our Own Tree

[%inc test_mock_tree.py %]

</section>
<section class="slide" markdown="1">

## Running Tests

[%inc test_hash_all.py omit=change %]

</section>
<section class="slide" markdown="1">

## Tracking Backups

-   Store backups and manifests in a directory selected by the user

    -   Real system would support remote storage as well

    -   Which suggests we need to design with multiple back ends in mind

-   Backed-up files are `abcd1234.bck`

-   Manifests are `ssssssssss.csv`,
    where `ssssssssss` is the [%g utc "UTC" %] [%g timestamp "timestamp" %]

</section>
<section class="slide" markdown="1">

## Race Condition

-   Manifest naming scheme fails if we try to create two backups in less than one second

-   A [%g toctou "time of check/time of use" %] [%g race_condition "race condition" %]

-   May seem unlikely, but many bugs and security holes seemed unlikely to their creators

</section>
<section class="slide" markdown="1">

## Creating a Backup

[%inc backup.py mark=backup %]

-   An example of [%g successive_refinement "successive refinement" %]

</section>
<section class="slide" markdown="1">

## Writing the Manifest

-   Create the backup directory if it doesn't already exist

    -   Another race condition

-   Then save CSV

[%inc backup.py mark=write %]

</section>
<section class="slide" markdown="1">

## Saving Files

[%inc backup.py mark=copy %]

-   Yet another race condition

</section>
<section class="slide" markdown="1">

## Setting Up for Testing

[%inc test_backup.py mark=setup %]

</section>
<section class="slide" markdown="1">

## A Sample Test

[%inc test_backup.py mark=test %]

-   Trust that the hash is correct

-   Should look inside the manifest and check that it lists files correctly

</section>
<section class="slide" markdown="1">

## Refactoring

-   Create a [%g base_class "base class" %] with the general steps

[%inc backup_oop.py mark=base %]

-   Derive a [%g child_class "child class" %] to do local archiving

-   Convert functions we have built so far into methods

</section>
<section class="slide" markdown="1">

## Refactoring

-   Can then create the specific archiver we want

[%inc backup_oop.py mark=create %]

-   Other code can then use it *without knowing exactly what it's doing*

[%inc backup_oop.py mark=use %]

</section>
<section class="slide" markdown="1">

## Summary	       

[% figure
   slug="archive-concept-map"
   img="concept_map.svg"
   alt="Concept map of build manager"
   caption="Concept map."
%]

</section>
