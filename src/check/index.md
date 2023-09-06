---
syllabus:
-   HTML consists of text and of elements represented by tags with attributes.
-   HTML is represented in memory as a Document Object Model (DOM) tree.
-   Trees are usually processed using recursion.
-   The Visitor design pattern is often used to perform an action for each member of a data structure.
-   We can summarize and check the structure of an HTML page by visiting each node and recording what we find there.
depends:
-   parse
---

Suppose we want to generate web pages to show the results of data analyses.
We want to check that these pages all have the same structure
so that people can find things in them,
and that they meet accessibility standards
so that *everyone* can find things in them.
This chapter builds a small tool to do this checking,
which introduces ideas we will use in building a page generator ([%x template %])
and another to check the structure and style of our code ([%x lint %]).

## HTML and the DOM {: #check-htmldom}

An [%g html "HTML" %] document is made up of [%g element "elements" %] and text.
(It can actually contain other things, but we'll ignore those for now.)
Elements are represented using [%g tag "tags" %] enclosed in `<` and `>`.
An [%g tag_opening "opening tag" %] like `<p>` starts an element,
while a [%g tag_closing "closing tag" %] like `</p>` ends it.
If the element is empty,
we can use a [%g tag_self_closing "self-closing tag" %] like `<br/>`
to save some typing.
Tags must be properly nested,
i.e.,
they must be closed in the reverse of the order in which they were opened.
This rule means that things like `<a><b></a></b>` are not allowed;
it also means that
a document's elements form a [%g tree "tree" %] of [%g node "nodes" %] and text
like the one shown in [%f check-dom-tree %].

This figure also shows that
opening and self-closing tags can have [%g attribute "attributes" %],
which are written as `key="value"`.
For example,
if we want to put an image in an HTML page
we specify the image file's name using the `src` attribute of the `img` tag:

```
<img src="banner.png" />
```

[% figure
   slug="check-dom-tree"
   img="dom_tree.svg"
   alt="DOM tree"
   caption="Representing HTML elements as a DOM tree."
%]

The objects that represent the nodes and text in an HTML tree
are called the Document Object Model or [%g dom "DOM" %].
Hundreds of tools have been written to convert HTML text to DOM;
our favorite is a Python module called [Beautiful Soup][beautiful_soup],
which can handle messy real-world documents
as well as those that conform to every rule of the standard.

Beautiful Soup's DOM has two main classes:
`NavigableString` for text and `Tag` for elements.
To parse a document,
we import what we need and call `BeautifulSoup` with
the text to be [%i "parser" "parsed" %]
and a string specifying exactly what kind of parsing we want to do.
(In practice, this is almost always `"html.parser"`.)

[% inc file="parse.py" keep="main" %]

`Tag` nodes have two properties `name` and `children`
to tell us what element the tag represents
and to give us access to the node's [%g child_tree "children" %],
i.e.,
the nodes below it in the tree.
We can therefore write a short [%i "recursion" "recursive" %] function
to show us everything in the DOM:

[% inc file="parse.py" keep="display" %]

We can test this function with a short example:

[% inc file="parse.py" keep="text" %]
[% inc file="parse.out" %]

In order to keep everything in one file,
we have written the HTML "page" as a multiline Python string;
we will do this frequently when writing unit tests
so that the HTML [%i "fixture" %] is right beside the test code.
Notice in the output that the line breaks in the HTML
have been turned into text nodes containing only a newline character `"\n"'.
It's easy to forget about these when writing code that processes pages.
{: .continue}

The last bit of the DOM that we need is its representation of attributes.
Each `Tag` node has a [%i "dictionary" %] called `attrs`
that stores the node's attributes.
The values in this dictionary are either strings or lists of strings
depending on whether the attribute has a single value or multiple values:

[% inc file="attrs.py" keep="display" %]
[% inc file="attrs.py" keep="text" %]
[% inc file="attrs.out" %]

## The Visitor Pattern {: #check-visitor-pattern}

Before building an HTML validator,
let's build something to tell us
which elements appear inside which others in a document.
Our recursive function takes two arguments:
the current node and a dictionary
whose keys are node names and whose values are sets
containing the names of those nodes' children.
Each time it encounters a node,
the function adds the names of the child nodes to the appropriate set
and then calls itself once for each child to collect their children:

[% inc file="contains.py" keep="recurse" %]

When we run our function on this page:

[% inc file="page.html" %]

it produces this output
(which we print in sorted order to make things easier to find):
{: .continue}

[% inc file="contains.out" %]

At this point have written several recursive functions
that have almost exactly the same [%i "control flow" %].
A good rule of software design is that if we have built something three times
we should make what we've learned reusable
so that we never have to write it again.
In this case,
we will rewrite our code to use the [%g visitor_pattern "Visitor" %] [%i "design pattern" %].

A visitor is a [%i "class" %] that knows how to get to each element of a data structure
and call a user-defined [%i "method" %] when it gets there.
Our visitor will have three methods:
one that it calls when it first encounters a node,
one that it calls when it is finished with that node,
and one that it calls for text ([%f check-visitor %]):

[% inc file="visitor.py" keep="visitor" %]

We provide do-nothing implementations of the three action methods
rather than having them [%i "raise" %] a `NotImplementedError`
because a particular use of our `Visitor` class may not need some of these methods.
For example,
our catalog builder didn't need to do anything when leaving a node or for text nodes,
and we shouldn't require people to implement things they don't need.
{: .continue}

[% figure
   slug="check-visitor"
   img="visitor.svg"
   alt="Visitor pattern order of operations"
   caption="Visitor checking each node in depth-first order."
%]

Here's what our catalog builder looks like
when reimplemented on top of our `Visitor` class:

[% inc file="catalog.py" keep="visitor" %]
[% inc file="catalog.py" keep="main" %]

It is only a few lines shorter than the original,
but the more complicated the data structure is,
the more helpful the Visitor pattern becomes.

## Checking Style {: #check-style}

To wrap up our style checker,
let's create a [%i "manifest" %] that specifies
which types of nodes can be children of which others:

[% inc file="manifest.yml" %]

We've chosen to use [%i "YAML" %]
for the manifest
because it's a relatively simple way to write nested rules.
[%i "JSON" %] would have worked just as well,
but as we said in [%x parse %],
we shouldn't invent a syntax of our own:
there are already too many in the world.
{: .continue}

Our `Check` class needs a [%i "constructor" %] to set everything up
and a `_tag_enter` method to handle nodes:

[% inc file="check.py" keep="check" %]

To run this,
we load a manifest and an HTML document,
create a checker,
ask the checker to visit each node,
then print out every problematic parent-child combination it found:

[% inc file="check.py" keep="main" %]
[% inc file="check.out" %]

The output tells us that content is supposed to be inside a `section` element,
not directly inside the `body`,
and that we're not supposed to *emphasize* words in lists.
Other users' rules may be different,
but we now have the tool we need
to check that any HTML we generate conforms to our intended rules.
More importantly,
we have a general pattern for building recursive code
that we can use in upcoming chapters.

## Summary {: #check-summary}

[% figure
   slug="check-concept-map"
   img="concept_map.svg"
   alt="Concept map for checking HTML"
   caption="Concept map for checking HTML using the Visitor pattern."
   cls="here"
%]

## Exercises {: #check-exercises}

### Simplify the Logic {: .exercise}

1.  Trace the operation of `Check._tag_enter`
    and convince yourself that it does the right thing.

2.  Rewrite it to make it easier to understand.

### Detecting Empty Elements {: .exercise}

Write a visitor that builds a list of nodes
that could be written as self-closing tags but aren't,
i.e.,
node that are written as `<a></a>`.
The `Tag.sourceline` attribute may help you
make your report more readable.

### Eliminating Newlines {: .exercise}

Write a visitor that deletes any text nodes from a document
that only contain newline characters.
Do you need to make any changes to `Visitor`,
or can you implement this using the class as it is?

### Linearize the Tree {: .exercise}

Write a visitor that returns a flat list containing
all the nodes in a [%g dom_tree "DOM tree" %]
in the order in which they would be traversed.
When you are done,
you should be able to write code like this:

```python
for node in Flatten(doc.html).result():
    print(node)
```

### Reporting Accessibility Violations {: .exercise}

1.  Write a program that reads one or more HTML pages
    and reports images in them that do *not* have an `alt` attribute.

2.  Extend your program so that it also reports
    any `figure` elements that do *not* contain exactly one `figcaption` element.

3.  Extend your program again so that it warns about images with redundant text
    (i.e., images in figures
    whose `alt` attribute contains the same text
    as the figure's caption).

### Ordering Headings {: .exercise}

Write a program that checks the ordering of headings in a page:

1.  There should be exactly one `h1` element,
    and it should be the first heading in the page.

2.  Heading levels should never increase by more than 1,
    i.e.,
    an `h1` should only ever be followed by an `h2`,
    an `h2` should never be followed directly by an `h4`,
    and so on.

### Report Full Path {: .exercise}

Modify the checking tool so that it reports
the full path for style violations when it finds a problem,
e.g.,
reports 'div.div.p`
(meaning "a paragraph in a div in another div")
instead of just `p`.
