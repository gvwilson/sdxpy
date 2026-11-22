---
title: "A Database"
---

<section class="slide" markdown="1">

## The Problem

-   Persisting objects ([%x persist %]) lets us save and restore program state

-   But we often want fast lookup *without* reloading all the data

-   And interoperability across languages

-   Create a simple [%g log_structured_db "log-structured database" %]

</section>
<section class="slide" markdown="1">

## Starting Point

-   A simple [%g key_value_store "key-value store" %] that lets us look things up

-   User must provide a function that gets key from record

[%inc interface_original.py %]

</section>
<section class="slide" markdown="1">

## Just a Dictionary

-   Store in memory using a dictionary

[%inc just_dict_original.py %]

-   Lets us start writing tests

</section>
<section class="slide" markdown="1">

## Experimental Records

[%inc record_original.py omit=omit %]

</section>
<section class="slide" markdown="1">

## Test Fixtures

-   Use the `pytest.fixture` decorator from [%x func %]

[%inc test_db_original.py mark=fixture %]

</section>
<section class="slide" markdown="1">

## Tests

[%inc test_db_original.py mark=test %]

</section>
<section class="slide" markdown="1">

## Refactor Interface

-   We're going to need other record manipulation functions

-   So save the record class instead of the key function

[%inc interface.py %]

</section>
<section class="slide" markdown="1">

## Refactor Database

-   Corresponding change to use a [%g static_method "static method" %]
    of the record class

[%inc just_dict_refactored.py %]

</section>
<section class="slide" markdown="1">

## Saving Records

-   Records must know how to pack and unpack themselves

-   Start by calculating the size of each

[%inc record.py mark=base %]

</section>
<section class="slide" markdown="1">

## Packing

[%inc record.py mark=pack %]

-   Save as strings with [%g null_byte "null byte" %] `\0` between them

-   A real implementation would pack as binary ([%x binary %])

</section>
<section class="slide" markdown="1">

## Unpacking

[%inc record.py mark=unpack %]

-   Note: this doesn't handle strings with null bytes

    -   A real implementation would etc.

-   Methods for packing and unpacking multiple records are straightforward

</section>
<section class="slide" markdown="1">

## A File-Backed Database

[% figure
   slug="db-single-file"
   img="single_file.svg"
   alt="Using a single file"
   caption="Saving the entire database in a single file."
%]

</section>
<section class="slide" markdown="1">

## A File-Backed Database

[%inc file_backed.py mark=core %]

-   Needs two [%g helper_method "helper methods" %]

</section>
<section class="slide" markdown="1">

## A File-Backed Database

[%inc file_backed.py mark=helper %]

-   Still saving and loading entire database

-   But look at all the infrastructure we've built

</section>
<section class="slide" markdown="1">

## Saving Blocks

-   Save *N* records per [%g block_memory "block" %]

-   Keep the [%g index_database "index" %] in memory

-   When writing, only modify one block (smaller and faster)

-   When reading, only load one block (ditto)

</section>
<section class="slide" markdown="1">

## Allocating Blocks

[% figure
   slug="db-alloc"
   img="alloc.svg"
   alt="Mapping records to blocks"
   caption="Mapping records to blocks."
%]

</section>
<section class="slide" markdown="1">

## Store Blocks in Memory

[%inc blocked.py mark=class %]

</section>
<section class="slide" markdown="1">

## Adding a Record

[%inc blocked.py mark=add %]

-   Get the sequence ID for this record

-   Store the key-to-sequence mapping in the index

-   Find or create the right block

-   Add the record

</section>
<section class="slide" markdown="1">

## Getting a Record

[%inc blocked.py mark=get %]

-   Do we even know about this record?

-   Find its current sequence ID

-   Find the corresponding block

-   Get the record

</section>
<section class="slide" markdown="1">

## Helper Methods

[%inc blocked.py mark=helper %]

</section>
<section class="slide" markdown="1">

## Persisting Blocks

-   Use inheritance to do everything described above while saving and loading blocks

[%inc blocked_file.py mark=class %]

</section>
<section class="slide" markdown="1">

## Saving

[%inc blocked_file.py mark=save %]

-  Have to pack and save all the records in the block

</section>
<section class="slide" markdown="1">

## Loading

[%inc blocked_file.py mark=load %]

-   Unpack all the records in the block

</section>
<section class="slide" markdown="1">

## Why Split Loading?

-   Need to initialize the in-memory index when restarting the database

[%inc blocked_file.py mark=index %]

-   Obvious extension: save the index in another file

-   Would have to profile ([%x perf %]) to see if this was worthwhile

</section>
<section class="slide" markdown="1">

## Next Steps

-   Clean up unused files

-   [%g compact "Compact" %] storage periodically

-   Use other data structures for indexing

</section>
<section class="slide" markdown="1">

## Summary

[% figure
   slug="db-concept-map"
   img="concept_map.svg"
   alt="Concept map for database"
   caption="Concept map."
%]

</section>
