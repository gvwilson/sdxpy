---
syllabus:
-   A layout engine determines where to place text and other page elements based on their size and organization.
-   Page elements are organized as a tree of basic blocks, rows, and columns.
-   The layout engine calculates the position of each block based on its size and the position of its parent.
-   Drawing blocks on top of each other from top to bottom is an easy way to render them.
-   Use multiple inheritance and mixin classes to inject methods into classes without modifying their parent class.
---

You might be reading this as HTML in your browser,
as an e-book (which is basically the same thing),
or on the printed page.
In all three cases
a [%i "layout engine" %][%g layout_engine "layout engine" %][%/i%] took some text and some layout instructions
and decided where to put each character and image.
To explore how they work,
we will build a small layout engine
based on [%i "Brubeck, Matt" %][Matt Brubeck's][brubeck_matt][%/i%] [tutorial][browser_engine_tutorial]
and on [Pavel Panchekha][panchekha_pavel] and [Chris Harrelson's][harrelson_chris]
[*Web Browser Engineering*][browser_engineering].
Since our focus is layout rather than parsing,
we will create objects in memory that represent [%i "DOM" %]DOM[%/i%] nodes
to test our ideas.

<div class="callout" markdown="1">

### Upside Down

The [%i "coordinate system" %]coordinate systems[%/i%] for screens
puts (0, 0) in the upper left corner instead of the lower left.
X increases to the right as usual,
but Y increases as we go down, rather than up
([%f layout-coordinate-system %]).
This convention is a holdover from the days of teletype terminals
that printed lines on rolls of paper;
as [%i "Hoye, Mike" %][Mike Hoye][hoye_mike][%/i%] has [observed][punching_holes],
the past is all around us.

</div>

[% figure
   slug="layout-coordinate-system"
   img="coordinate_system.svg"
   alt="Coordinate system"
   caption="Coordinate system with (0, 0) in the upper left corner."
%]

## Sizing {: #layout-size}

Let's start on [%g easy_mode "easy mode" %]
without margins, padding, line-wrapping, or other complications.
Everything we can put on the screen is represented as a rectangular cell,
and every cell is either a row, a column, or a block.
A block has a fixed width and height:

[% inc file="easy_mode.py" keep="block" %]

A row arranges one or more cells horizontally;
its width is the sum of the widths of its children,
while its height is the height of its tallest child
([%f layout-sizing %]):

[% inc file="easy_mode.py" keep="row" %]

[% figure
   slug="layout-sizing"
   img="sizing.svg"
   alt="Calculating sizes of fixed blocks"
   caption="Calculating sizes of blocks with fixed width and height."
%]

Finally,
a column arranges one or more cells vertically:
its width is the width of its widest child
and its height is the sum of the heights of its children.
(Here and elsewhere we use the abbreviation `col` when referring to columns.)

[% inc file="easy_mode.py" keep="col" %]

Rows and columns nest inside one another:
a row cannot span two or more columns,
and a column cannot cross the boundary between two rows.
We can therefore represent our document as a tree
and calculate the width and height of each cell every time we need it.
This is simple but inefficient:
we could calculate both width and height at the same time
and [%i "cache!calculated values" %][%g cache "cache" %][%/i%] those values to avoid recalculation,
but we called this "easy mode" for a reason.

As simple as it is,
this code could still contain errors (and did during development),
so we write some tests to check that it works as desired
before trying to build anything more complicated:

[% inc pat="test_easy_mode.*" fill="py out" %]

## Positioning {: #layout-position}

Once we know how big cells are we can figure out where to put them.
Suppose we start with the upper left corner of the browser:
upper because we lay out the page top-to-bottom
and left because we are doing left-to-right layout.
If the cell is a block, we place it there.
If the cell is a row, on the other hand,
we get its height
and then calculate its lower edge as y1 = y0 + height.
We then place the first child's upper-left corner at (x0, y1),
the second child's at (x0 + width0, y1), and so on
([%f layout-layout %]).
Similarly,
if the cell is a column
we place the first child at (x0, y0),
the next at (x0, y0 + height0),
and so on.

[% figure
   slug="layout-layout"
   img="layout.svg"
   alt="Laying out rows and columns"
   caption="Laying out rows and columns of fixed-size blocks."
%]

To save ourselves some work we will derive the classes that know how to do layout
from the classes we wrote before.
Our blocks are:

[% inc file="placed.py" keep="block" %]

while our columns are:
{: .continue}

[% inc file="placed.py" keep="col" %]

and our rows are:
{: .continue}

[% inc file="placed.py" keep="row" %]

Once again,
we write and run some tests to check that everything is doing what it's supposed to:

[% inc file="test_placed.py" omit="large" %]
[% inc file="test_placed.out" %]

## Rendering {: #layout-render}

We drew blocks on graph paper
to figure out the expected answers for the tests shown above.
We can do something similar in software by creating a "screen" of space characters
and then having each block draw itself in the right place.
If we do this starting at the root of the tree,
child blocks will overwrite the markings made by their parents,
which will automatically produce the right appearance
([%f layout-draw-over %]).
(A more sophisticated version of this called [%g z_buffering "z-buffering" %]
keeps track of the visual depth of each pixel
in order to draw things in three dimensions.)

[% figure
   slug="layout-draw-over"
   img="draw_over.svg"
   alt="Children drawing over their parents"
   caption="Render blocks by drawing child nodes on top of parent nodes."
%]

Our pretended screen is just an array of arrays of characters:

[% inc file="render.py" keep="make_screen" %]

We will use successive lower-case characters to show each block,
i.e.,
the root block will draw itself using 'a',
while its children will be 'b', 'c', and so on.
{: .continue}

[% inc file="render.py" keep="draw" %]

To teach each kind of cell how to render itself,
we have to derive a new class from each of the ones we have
and give the new class a `render` method with the same
[%i "signature!of function" "function signature" %][%g signature "signature" %][%/i%].
Since Python supports [%i "multiple inheritance" %][%g multiple_inheritance "multiple inheritance" %][%/i%],
we can do this with a [%i "mixin class" %][%g mixin "mixin" %][%/i%] class
([%f layout-mixin %]):

[% inc file="rendered.py" %]

[% figure
   slug="layout-mixin"
   img="mixin.svg"
   alt="Adding methods with a mixin class"
   caption="Using multiple inheritance and a mixin class to add methods."
%]

<div class="callout" markdown="1">

### (Not) The Right Way to Do It

If we were building a real layout engine,
a cleaner solution would be to go back and create
a class called `Cell` with this `render` method,
then derive our `Block`, `Row`, and `Col` classes from that.
In general,
if two or more classes need to be able to do something,
we should add a method to do that to their lowest common ancestor.

</div>

Our simpler tests are a little easier to read using rendering,
though we still had to draw things on paper to figure out our complex ones:

[% inc file="test_rendered.py" keep="large" %]

The fact that our tests are difficult to understand
is a sign that we should do more testing
It would be very easy for us to get a wrong result
and convince ourselves that it was actually correct;
[%i "confirmation bias" %][%g confirmation_bias "confirmation bias" %][%/i%] of this kind
is very common in software development.
{: .continue}

## Wrapping {: #layout-fit}

One of the biggest differences between a browser and a printed page
is that the text in the browser wraps automatically as the window is resized.
(The other, these days, is that the printed page doesn't spy on us,
though someone is undoubtedly working on that.)

To add wrapping to our layout engine,
suppose we fix the width of a row.
If the total width of the children is greater than the row's width,
the layout engine needs to wrap the children around.
This assumes that columns can be made as tall as they need to be,
i.e.,
that we can grow vertically to make up for limited space horizontally.
It also assumes that none of a row's children is wider than the width of the row
so that each can fit in a row of its own if necessary.
We will look at what happens when this isn't true in the exercises.

Our layout engine manages wrapping by transforming the tree.
The height and width of blocks are fixed,
so they become themselves.
Columns become themselves as well,
but since they have children that might need to wrap,
the class representing columns needs a new method:

[% inc file="wrapped.py" keep="blockcol" %]

Rows do all the hard work.
Each original row is replaced with a new row
that contains a single column with one or more rows,
each of which is one "line" of wrapped cells
([%f layout-wrap %]).
This replacement is unnecessary when everything will fit on a single row,
but it's easiest to write the code that does it every time;
we will look at making this more efficient in the exercises.

[% figure
   slug="layout-wrap"
   img="wrap.svg"
   alt="Wrapping rows"
   caption="Wrapping rows by introducing a new row and column."
%]

Our new wrappable row's constructor takes a fixed width followed by the children
and returns that fixed width when asked for its size:

[% inc file="wrapped.py" keep="row" omit="wrap" %]

Wrapping puts the row's children into buckets,
then converts the buckets to a row of a column of rows:
{: .continue}

[% inc file="wrapped.py" keep="wrap" %]

Once again we bring forward all the previous tests
and write some new ones to test the functionality we've added:

[% inc file="test_wrapped.py" keep="example" %]
[% inc file="test_wrapped.out" %]

Note that we could have had columns handle resizing rather than rows,
but we (probably) don't need to make both resizeable.
This is an example of [%g intrinsic_complexity "intrinsic complexity" %]:
the problem really is this hard,
so something, somewhere, has to deal with it.
(Programs often contain [%g accidental_complexity "accidental complexity" %]
as well,
which can be fixed if people are willing to accept that it is unnecessary
and are willing to change.
In practice,
these requirements usually mean that it isn't ever fixed.)

<div class="callout" markdown="1">

### The Liskov Substitution Principle

We are able to re-use tests as our code evolved
because of the [%i "Liskov Substitution Principle" "software design!Liskov Substitution Principle" %][%g liskov_substitution_principle "Liskov Substitution Principle" %][%/i%],
which states that
it should be possible to replace objects in a program
with objects of derived classes
without breaking anything.
In order to satisfy this principle,
new code must handle the same set of inputs as the old code,
though it may be able to process more inputs as well.
Conversely,
its output must be a subset of what the old code produced
so that whatever is downstream from it won't be surprised.
Thinking in these terms leads to a methodology called
[%i "design by contract" "software design!design by contract" %][%g design_by_contract "design by contract" %][%/i%].

</div>

## Summary {: #layout-summary}

[% figure
   slug="layout-concept-map"
   img="concept_map.svg"
   alt="Concept map for page layout"
   caption="Page layout concept map."
%]

## Exercises {: #layout-exercises}

### Refactoring {: .exercise}

Refactor the classes used to represent blocks, rows, and columns so that:

1.  They all derive from a common parent.

2.  All common behavior is defined in that parent (if only with placeholder methods).

### Recycling {: .exercise}

Modify the wrapping code so that new rows and columns are only created if needed.
For example,
if a row of width 10 contains a text node that is only 4 characters wide,
a new row and column are *not* inserted.

### Rendering a Clear Background {: .exercise}

Modify the rendering code so that only the text in block nodes is shown,
i.e.,
so that the empty space in rows and columns is rendered as spaces.

### Clipping Text {: .exercise}

1.  Modify the wrapping and rendering so that
    if a block of text is too wide for the available space
    the extra characters are clipped.
    For example,
    if a column of width 5 contains a line "unfittable",
    only "unfit" appears.

2.  Extend your solution to break lines on spaces as needed
    in order to avoid clipping.

### Bidirectional Rendering {: .exercise}

Modify the existing software to do either left-to-right or right-to-left rendering
upon request.

### Equal Sizing {: .exercise}

Modify the existing code to support elastic columns,
i.e.,
so that all of the columns in a row are automatically sized to have the same width.
If the number of columns does not divide evenly into the width of the row,
allocate the extra space as equally as possible from left to right.

### Drawing Borders {: .exercise}

1.  Modify the existing code so that elements are drawn with borders like this:

    ```txt
    +----+
    |text|
    +----+
    ```

### Padding Elements {: .exercise}

Modify the existing code so that:

1.  Authors can define a `padding` attribute for row and column elements.

2.  When the node is rendered, that many blank spaces are added on all four sides of the contents.

For example, string `"text"` with a padding of 1 would render as:
{: .continue}

```txt
+------+
|      |
| text |
|      |
+------+
```

where the lines show the outer border of the rendering.
{: .continue}

### Properties {: .exercise}

Look at the documentation for Python's [`@property`][py_property] decorator
and modify the block classes to replace the `get_width` and `get_height` methods
with properties called `width` and `height`.

### Tables {: .exercise}

Add another node type `Table` such that:

1.  All the children of a table must be rows.

2.  Every row must contain exactly the same number of columns.

3.  When the table is rendered, every column has the same width in every row.
