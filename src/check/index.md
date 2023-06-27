---
syllabus:
-   FIXME
depends:
-   parse
---

Suppose we want to generate HTML summaries of experiments.
We want to be sure the generated pages have the right structure
so that people can get information out of them reliably.
We also want to make sure that they meet accessibility standards
so that *everyone* can get information out of them.
In short,
we want the equivalent of unit tests for our output.

This chapter builds a small tool to check the structure of HTML.
Doing this prepares us for building a tool to generate pages ([%x template %])
and another to check the structure and style of our code ([%x lint %]).

## HTML and the DOM {: #check-htmldom}

An HTML document is made up of [%g element "elements" %] and text.
(It can actually contain other things, but we'll ignore those for now.)
Elements are represented using [%g tag "tags" %] enclosed in `<` and `>`.
An [%g tag_opening "opening tag" %] like `<p>` starts an element,
while a [%g tag_closing "closing tag" %] like `</p>` ends it.
If the element is empty,
we can use a [%g tag_self_closing "self-closing tag" %] like `<br/>`
to save some typing.
Opening and self-closing tags can have [%g attribute "attributes" %],
which are written as `key="value"`.

Tags must be properly nested,
which has two consequences:

1.  Something like `<a><b></a></b>` is illegal.

2.  A document's elements form a [%g tree "tree" %] of [%g node "nodes" %] and text
    like the one shown in [%f check-dom-tree %].

[% figure
   slug="check-dom-tree"
   img="dom_tree.svg"
   alt="DOM tree"
   caption="Representing HTML elements as a DOM tree."
%]

The objects that represent the nodes and text in an HTML tree
are called the [%g dom "Document Object Model" %], or DOM.
Hundreds of tools have been written to convert HTML text to DOM;
our favorite is a Python library called [Beautiful Soup][beautiful_soup],
which can handle messy real-world documents
as well as those that conform to every rule of the standard.

Beautiful Soup's DOM has two main classes:
`NavigableString` for text and `Tag` for elements.
To parse a document,
we import what we need and call `BeautifulSoup` with
the text to be parsed
and a string specifying exactly what kind of parsing we want to do.
(In practice, this is almost always `"html.parser"`.)

[% inc file="parse.py" keep="main" %]

`Tag` nodes have two properties `name` and `children`
to tell us what element the tag represents
and to give us access to the node's [%g child_tree "children" %],
i.e.,
the nodes below it in the tree.
We can therefore write a short recursive function
to show us everything in the DOM:

[% inc file="parse.py" keep="display" %]

We can test this with a short example:

[% inc file="parse.py" keep="text" %]
[% inc file="parse.out" %]

Notice that all of the newlines in our document
have been preserved as text nodes.
{: .continue}

Finally,
each `Tag` node has a dictionary called `attrs`
that stores the attributes of that node.
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
the function adds its children's names to the appropriate set
and then calls itself:

[% inc file="contains.py" keep="recurse" %]

When we run our function on this page:

[% inc file="page.html" %]

it produces this output
(which we print in sorted order to make things easier to find):
{: .continue}

[% inc file="contains.out" %]

We have written several recursive functions already,
all of which have more or less the same [%i "control flow" %][%/i%].
A good rule of software design is that if we have written something three times,
we should turn what we've learned into something reusable
so that we never have to write it again.
In this case,
we can use the [%g visitor_pattern "Visitor" %] design pattern.
A visitor is a class that knows how to get to each element of a data structure
and call a user-defined method when it gets there.
Our visitor will have three methods:
one that it calls when it first encounters a node,
one that it calls when it is finished with that node,
and one that it calls for text ([%f check-visitor %]):

[% inc file="visitor.py" keep="visitor" %]

Notice that we provide do-nothing implementations of these three methods
rather than having them raise a `NotImplementedError`.
A particular use of our `Visitor` class may not need some of these methods—for example,
our catalog builder didn't need to do anything when leaving a node or for text nodes—and
we shouldn't require people to implement things they don't need.
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
let's create a [%i "manifest" %][%/i%] that specifies
which types of nodes can be children of which others:

[% inc file="manifest.yml" %]

We've chosen to use [%i "YAML" %][%/i%] for the manifest
because it's a relatively simple way to write nested rules.
We could have used [%i "JSON" %][%/i%],
but as we said in [%x parse %],
we shouldn't invent a syntax of our own:
there are already too many in the world.
{: .continue}

Our `Check` class only needs a constructor to set everything up
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

## Summary {: #check-summary}

[% figure
   slug="check-concept-map"
   img="concept_map.svg"
   alt="Concept map for checking HTML"
   caption="Concept map for checking HTML using the Visitor pattern."
%]

## Exercises {: #check-exercises}

### Simplify the Logic

1.  Trace the operation of `Check._tag_enter`
    and convince yourself that it does the right thing.

2.  Rewrite it to make it easier to understand.

### Detecting Empty Elements

Write a visitor that builds a list of nodes
that could be written as self-closing tags but aren't,
i.e.,
node that are written as `<a></a>`.
The `Tag.sourceline` attribute may help you
make your report more readable.

### Eliminating Newlines

Write a visitor that deletes any text nodes from a document
that only contain newline characters.
Do you need to make any changes to `Visitor`,
or can you implement this using the class as it is?

### Linearize the Tree

Write a visitor that returns a flat list containing
all the nodes in a DOM tree
in the order in which they would be traversed.
When you are done,
you should be able to write code like this:

```python
for node in Flatten(doc.html).result():
    print(node)
```
