---
template: slides
title: "A Database"
---

## The Problem

-   Persisting objects ([%x persist %]) lets us save and restore program state

-   But we often want fast lookup *without* reloading all the data

-   And interoperability across languages

-   Create a simple [%g log_structured_db "log-structured database" %]

---

## Starting Point

-   A simple [%g key_value_store "key-value store" %] that lets us look things up

-   User must provide a function that gets key from record

[%inc interface_original.py %]

---

## Just a Dictionary

-   Store in memory using a dictionary

[%inc just_dict_original.py %]

-   Lets us start writing tests

---

## Experimental Records

[%inc record_original.py omit=omit %]

---

## Test Fixtures

-   Use the `pytest.fixture` decorator from [%x func %]

[%inc test_db_original.py mark=fixture %]

---

## Tests

[%inc test_db_original.py mark=test %]

---

## Refactor Interface

-   We're going to need other record manipulation functions

-   So save the record class instead of the key function

[%inc interface.py %]

---

## Refactor Database

-   Corresponding change to use a [%g static_method "static method" %]
    of the record class

[%inc just_dict_refactored.py %]

---

## Saving Records

-   Records must know how to pack and unpack themselves

-   Start by calculating the size of each

[%inc record.py mark=base %]

---

## Packing

[%inc record.py mark=pack %]

-   Save as strings with [%g null_byte "null byte" %] `\0` between them

-   A real implementation would pack as binary ([%x binary %])

---

## Unpacking

[%inc record.py mark=unpack %]

-   Note: this doesn't handle strings with null bytes

    -   A real implementation would etc.

-   Methods for packing and unpacking multiple records are straightforward

---

## A File-Backed Database

[% figure
   slug="db-single-file"
   img="single_file.svg"
   alt="Using a single file"
   caption="Saving the entire database in a single file."
%]

---

## A File-Backed Database

[%inc file_backed.py mark=core %]

-   Needs two [%g helper_method "helper methods" %]

---

## A File-Backed Database

[%inc file_backed.py mark=helper %]

-   Still saving and loading entire database

-   But look at all the infrastructure we've built

---

## Saving Blocks

-   Save *N* records per [%g block_memory "block" %]

-   Keep the [%g index_database "index" %] in memory

-   When writing, only modify one block (smaller and faster)

-   When reading, only load one block (ditto)

---

## Allocating Blocks

[% figure
   slug="db-alloc"
   img="alloc.svg"
   alt="Mapping records to blocks"
   caption="Mapping records to blocks."
%]

---

## Store Blocks in Memory

[%inc blocked.py mark=class %]

---

## Adding a Record

[%inc blocked.py mark=add %]

-   Get the sequence ID for this record

-   Store the key-to-sequence mapping in the index

-   Find or create the right block

-   Add the record

---

## Getting a Record

[%inc blocked.py mark=get %]

-   Do we even know about this record?

-   Find its current sequence ID

-   Find the corresponding block

-   Get the record

---

## Helper Methods

[%inc blocked.py mark=helper %]

---

## Persisting Blocks

-   Use inheritance to do everything described above while saving and loading blocks

[%inc blocked_file.py mark=class %]

---

## Saving

[%inc blocked_file.py mark=save %]

-  Have to pack and save all the records in the block

---

## Loading

[%inc blocked_file.py mark=load %]

-   Unpack all the records in the block

---

## Why Split Loading?

-   Need to initialize the in-memory index when restarting the database

[%inc blocked_file.py mark=index %]

-   Obvious extension: save the index in another file

-   Would have to profile ([%x perf %]) to see if this was worthwhile

---

## Next Steps

-   Clean up unused files

-   [%g compact "Compact" %] storage periodically

-   Use other data structures for indexing

---

<!--# class="summary" -->

## Summary

[% figure
   slug="db-concept-map"
   img="concept_map.svg"
   alt="Concept map for database"
   caption="Concept map for a log-structured database."
%]
