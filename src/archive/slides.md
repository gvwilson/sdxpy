---
template: slides
title: "A File Archiver"
---

## The Problem

-   Want to save snapshots of work in progress

-   Create a simple [%g version_control_system "version control system" %]

-   And show how to test it using mock objects ([%x protocols %])

---

## Design

-   Wasteful to store the same file repeatedly

-   So if the file's hash is `abcd1234`, save it as `abcd1234.bck`

    -   Handles renaming

-   Then create a [%g manifest "manifest" %] to show
    what unique blocks of bytes had what names when

---

## Storage

[% figure
   slug="archive-storage"
   img="storage.svg"
   alt="Backup file storage"
   caption="Organization of backup file storage."
%]

---

## Finding and Hashing

-   Use globbing ([%x glob %]) and hashing ([%x dup %])

[%inc hash_all.py mark=func %]

---

## Finding and Hashing

[%inc sample_dir.out %]
[%inc hash_all.sh %]
[%inc hash_all.out %]

---

## Testing

-   Obvious approach is to create lots of files and directories

-   But we want to test what happens when they change,
    which makes things complicated to maintain

-   Use a [%g mock_object "mock object" %] ([%x protocols %])
    instead of the real filesystem

---

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

---

## Direct Use

[%inc test_mock_fs.py %]

---

## Build Our Own Tree

[%inc test_mock_tree.py %]

---

## Running Tests

[%inc test_hash_all.py omit=change %]

---

## Tracking Backups

-   Store backups and manifests in a directory selected by the user

    -   Real system would support remote storage as well

    -   Which suggests we need to design with multiple back ends in mind

-   Backed-up files are `abcd1234.bck`

-   Manifests are `ssssssssss.csv`,
    where `ssssssssss` is the [%g utc "UTC" %] [%g timestamp "timestamp" %]

---

<!--# class="aside" -->

## Race Condition

-   Manifest naming scheme fails if we try to create two backups in less than one second

-   A [%g toctou "time of check/time of use" %] [%g race_condition "race condition" %]

-   May seem unlikely, but many bugs and security holes seemed unlikely to their creators

---

## Creating a Backup

[%inc backup.py mark=backup %]

-   An example of [%g successive_refinement "successive refinement" %]

---

## Writing the Manifest

-   Create the backup directory if it doesn't already exist

    -   Another race condition

-   Then save CSV

[%inc backup.py mark=write %]

---

## Saving Files

[%inc backup.py mark=copy %]

-   Yet another race condition

---

## Setting Up for Testing

[%inc test_backup.py mark=setup %]

---

## A Sample Test

[%inc test_backup.py mark=test %]

-   Trust that the hash is correct

-   Should look inside the manifest and check that it lists files correctly

---

## Refactoring

-   Create a [%g base_class "base class" %] with the general steps

[%inc backup_oop.py mark=base %]

-   Derive a [%g child_class "child class" %] to do local archiving

-   Convert functions we have built so far into methods

---

## Refactoring

-   Can then create the specific archiver we want

[%inc backup_oop.py mark=create %]

-   Other code can then use it *without knowing exactly what it's doing*

[%inc backup_oop.py mark=use %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="archive-concept-map"
   img="concept_map.svg"
   alt="Concept map of build manager"
   caption="Concept map."
%]
