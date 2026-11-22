---
title: "An HTML Validator"
---

<section class="slide" markdown="1">

## The Problem

-   We generate HTML pages to report experiments

-   Want to be sure they have the right structure
    so that people can get information out of them reliably

-   Learning how to do this prepares us for checking code

</section>
<section class="slide" markdown="1">

## HTML as Text

-   HTML documents contain [%g tag "tags" %] and text

-   An [%g tag_opening "opening tag" %] like `<p>` starts an element

-   A [%g tag_closing "closing tag" %] like `</p>` ends the element

-   If the element is empty,
    we can use a [%g tag_self_closing "self-closing tag" %] like `<br/>`

-   Opening and self-closing tags can have [%g attribute "attributes" %]

    -   Written as `key="value"` (with some variations)

-   Tags must be properly nested:
    `<a><b></a></b>` is illegal

</section>
<section class="slide" markdown="1">

## HTML as a Tree

-   HTML elements form a [%g tree "tree" %] of [%g node "nodes" %] and text

-   The object that represent these make up the [%g dom "Document Object Model" %] (DOM)

[% figure
   slug="check-dom-tree"
   img="dom_tree.svg"
   alt="DOM tree"
   caption="Representing HTML elements as a DOM tree."
%]

</section>
<section class="slide" markdown="1">

## From Text to DOM

-   Real-world HTML is often messy

-   Use [Beautiful Soup][beautiful_soup] to parse it

-   Nodes are `NavigableString` (for text) or `Tag` (for element)

-   `Tag` nodes have properties `name` and `children`

[%inc parse.py mark=main %]

</section>
<section class="slide" markdown="1">

## From Text to DOM

[%inc parse.py mark=text %]
[%inc parse.out %]

</section>
<section class="slide" markdown="1">

## Recursion

[%inc parse.py mark=display %]

-   Text nodes don't have children

-   `for child in node` loops over children of element nodes

</section>
<section class="slide" markdown="1">

## Attributes

-   A dictionary `node.attrs`

-   Can be single-valued or multi-valued

[%inc attrs.py mark=display %]

</section>
<section class="slide" markdown="1">

## Attributes

[%inc attrs.py mark=text %]
[%inc attrs.out %]

</section>
<section class="slide" markdown="1">

## Build a Catalog

-   What kinds of children do elements have?

    -   `<tr>` (table row) should only appear inside `<table>` or `<tbody>`

-   Recurse through DOM tree

[%inc contains.py mark=recurse %]

</section>
<section class="slide" markdown="1">

## Build a Catalog

[%inc page.html %]

</section>
<section class="slide" markdown="1">

## Build a Catalog

[%inc contains.out %]

</section>
<section class="slide" markdown="1">

## The Visitor Pattern

-   A [%g visitor_pattern "visitor" %] is a class
    that knows how to get to each element of a data structure

-   Derive a class of our own that does something for those elements

-   When we recurse, allow separate handlers for entry and exit

    -   Useful for things like pretty-printers

</section>
<section class="slide" markdown="1">

## The Visitor Pattern

[%inc visitor.py mark=visitor %]

-   `pass` rather than `NotImplementedError`
    because many uses won't need all these methods

</section>
<section class="slide" markdown="1">

## Catalog Reimplemented

[%inc catalog.py mark=visitor %]

-   Only a few lines shorter than the original

-   But the more complicated the data structure is,
    the more helpful the Visitor pattern becomes

</section>
<section class="slide" markdown="1">

## Catalog Reimplemented

[%inc catalog.py mark=main %]

</section>
<section class="slide" markdown="1">

## Visitor in Action

[% figure
   slug="check-visitor"
   img="visitor.svg"
   alt="Visitor pattern order of operations"
   caption="Visitor checking each node in depth-first order."
%]

</section>
<section class="slide" markdown="1">

## Find Style Violations

-   Compare each parent-child combination against a [%g manifest "manifest" %]

[%inc manifest.yml %]

</section>
<section class="slide" markdown="1">

## Find Style Violations

[%inc check.py mark=check %]

</section>
<section class="slide" markdown="1">

## Running the Checker

[%inc check.py mark=main %]

</section>
<section class="slide" markdown="1">

## Results

[%inc check.out %]

-   Because content is supposed to be inside a `section` tag,
    not directly in `body`

-   And we're not supposed to *emphasize* words in lists

</section>
<section class="slide" markdown="1">

## Summary

[% figure
   slug="check-concept-map"
   img="concept_map.svg"
   alt="Concept map for checking HTML"
   caption="Concept map."
%]

</section>
