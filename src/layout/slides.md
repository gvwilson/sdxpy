---
template: slides
title: "Page Layout"
---

## The Problem

-   Text is a sequence of characters, but a page is two-dimensional

-   How can we put the right things in the right places?

-   Create a simple version of a [%g layout_engine "layout engine" %] for a browser

-   But the same ideas apply to print

---

## Coordinate Systems

-   Teletypes started printing in the upper left corner of the page

-   So the coordinate systems for screens put (0, 0) in the upper left
    instead of the lower left

-   Y increases going *down*

-   At least X increases to the right as usual

[% figure
   slug="layout-coordinate-system"
   img="coordinate_system.svg"
   alt="Coordinate system"
   caption="Coordinate system with (0, 0) in the upper left corner."
%]

---

## Block Model

-   Every cell is a rectangular block

-   Row arranges sub-blocks horizontally

-   Column arranges sub-blocks vertically

[% figure
   slug="layout-sizing"
   img="sizing.svg"
   alt="Calculating sizes of fixed blocks"
   caption="Calculating sizes of blocks with fixed width and height."
%]

---

## Generic Block

[%inc easy_mode.py mark=block %]

-   Would calculate size based on contents (image, text, etc.)

---

## Rows

-   Width: sum of widths of children

-   Height: height of tallest child

[%inc easy_mode.py mark=row %]

---

## Columns

-   Width: width of widest child

-   Height: sum of heights of children

[%inc easy_mode.py mark=col %]

---

## Nesting

-   Rows can contain blocks and columns
    but must be contained in a single column (unless it's the root)

-   Columns can contain blocks or rows
    but must be contained in a single row (unless it's the root)

-   Can therefore represent document as a tree

[%inc test_easy_mode.py mark=example %]

---

## Positioning

-   Once we know sizes we can calculate positions

-   E.g., if cell is a row at `(x0, y0)`:

    -   Its lower edge is `y1 = y0 + height`

    -   Its first child's upper-left corner is `(x0, y1)`

    -   Second child's upper-left corner is `(x0 + width0, y1)`

[% figure
   slug="layout-layout"
   img="layout.svg"
   alt="Laying out rows and columns"
   caption="Laying out rows and columns of fixed-size blocks."
%]

---

## Positioning

[%inc placed.py mark=rowplace %]

---

## Rendering

-   Draw parents before children so that children over-draw

-   A simple form of [%g z_buffering "z-buffering" %]

[% figure
   slug="layout-draw-over"
   img="draw_over.svg"
   alt="Children drawing over their parents"
   caption="Render blocks by drawing child nodes on top of parent nodes."
%]

---

## Rendering

-   Create a character "screen"

[%inc render.py mark=make_screen %]

-   Add a method for blocks to draw

[%inc rendered.py mark=render %]

---

## Mixin Class

[% figure
   slug="layout-mixin"
   img="mixin.svg"
   alt="Adding methods with a mixin class"
   caption="Using multiple inheritance and a mixin class to add methods."
%]

---

## Wrapping

-   Fix width of row (for example)

-   If total width of children is greater than this,
    need to wrap the children to a new row

    -   Assuming no single child is too wide

-   Handle this by modifying the tree

[%inc wrapped.py mark=blockcol %]

---

## Wrapping Rows

[% figure
   slug="layout-wrap"
   img="wrap.svg"
   alt="Wrapping rows"
   caption="Wrapping rows by introducing a new row and column."
%]

---

## Wrapping Rows

-   New row class takes a fixed width and some children

-   Returns that fixed width when asked for its size

[%inc wrapped.py mark=row %]

---

## Wrapping Rows

-   Wrapping puts the row's children into buckets

-   Converts each bucket to a row with a column of rows

[%inc wrapped.py mark=wrap %]

---

## Bucketing

[%inc wrapped.py mark=bucket %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="layout-concept-map"
   img="concept_map.svg"
   alt="Concept map for page layout"
   caption="Page layout concept map."
%]
