---
abstract: >
    Writing and updating HTML pages by hand is time-consuming and error-prone,
    so most modern websites use some kind of static site generator (SSG)
    to create pages from templates.
    This chapter builds a simple SSG to show how they work
    and to reinforce earlier lessons about creating little programming languages.
syllabus:
-   Static site generators create HTML pages from templates, directives, and data.
-   A static site generator has the same core features as a programming language.
-   Special-purpose mini-languages quickly become as complex as mainstream languages.
-   Static methods are a convenient way to group functions together.
depends:
-   interp
-   check
---

Every program needs documentation,
and the best place to put documentation is on the web.
Writing and updating HTML pages by hand is time-consuming and error-prone,
particularly when many parts are the same.
Most modern websites therefore use some kind of
[%g static_site_generator "static site generator" %] (SSG)
to create pages from templates.

[Hundreds of SSGs][jamstack_ssg] have been written in every popular programming language,
and languages like [%i "PHP" url="php" %] have been invented primarily for this purpose.
Most of these systems use one of three designs
([%f template-options %]):

1.  Mix commands in an existing language such as JavaScript
    with the [%i "HTML" %] or [%i "Markdown" %]
    using some kind of marker to indicate which parts are commands
    and which parts are to be taken as-is.
    This approach is taken by [%i "EJS" url="ejs" %].

2.  Create a mini-language with its own commands like [%i "Jekyll" url="jekyll" %].
    Mini-languages are appealing because they are smaller and safer than general-purpose languages,
    but eventually they acquire most of the features of a general-purpose language.
    Again, some kind of marker must be used to show
    which parts of the page are code and which are ordinary text.

3.  Put directives in specially-named [%i "attribute" "attributes" %] in the HTML.
    This approach is the least popular,
    but it eliminates the need for a special [%i "parser" %].

[% figure
   slug="template-options"
   img="design_options.svg"
   alt="Three options for page templates"
   caption="Three different ways to implement page templating."
%]

This chapter builds a simple page templating system using the third strategy.
We will process each page independently by parsing the HTML
and walking the [%i "DOM" %] to find [%i "node" "nodes" %] with special attributes.
Our program will execute the instructions in those nodes
to implement loops and if/else statements;
other nodes will be copied as-is to create text.

## Syntax {: #template-syntax}

Let's start by deciding what "done" looks like.
Suppose we want to turn an array of strings into an HTML list.
Our template will look like this:

[% inc file="loop.ht" %]

The attribute `z-loop` tells the tool to repeat the contents of that node;
the loop variable and the collection being looped over are separated by a colon.
The `span` with the attribute `z-var`
tells the tool to fill in the node with the value of the variable.
When our tool processes this page,
the output will be standard HTML without any traces of how it was created:

[% inc file="loop.out" %]

<div class="callout" markdown="1">

### Human-Readable vs. Machine-Readable

Putting the loop variable and target in a single attribute
makes loops easy to type
but hides information from standard HTML tools,
which can't know that this attribute contains
multiple values separated by a colon.
We should use two attributes like this:

```html
<ul z-loop="names" z-loop-var="item">
```

but we decided to save ourselves a little typing.
We should also call our attributes `data-something` instead of `z-something`
to conform with the [%i "HTML5 specification" url="html5_data_attributes" %],
but again,
decided to save ourselves a bit of typing.
{: .continue}

</div>

The next step is to define the [%g api "Application Programming Interface" %] (API)
for filling in templates.
Our tool needs the template itself,
somewhere to write its output,
and the set of variables to use in the expansion.
Those variables might come from a configuration file
from a header in the file itself,
or from somewhere else entirely,
so we will assume the calling program has gotten them somehow
and have it pass them into the expansion function as a dictionary
([%f template-api %]):

[% inc file="example_call.py" %]

[% figure
   slug="template-api"
   img="api.svg"
   alt="Template API"
   caption="Combining text and data in templating."
   cls="here"
%]

## Managing Variables {: #template-values}

As soon as we have variables,
we need a way to track their values.
We also need to maintain multiple sets of variables
so that (for example) variables used inside a loop
don't conflict with ones used outside of it.
As in [%x interp %],
we will use a stack of [%i "environment" "environments" %],
each of which is a dictionary.

Our stack-handling class `Env` has methods
to push and pop new [%i "stack frame" "stack frames" %]
and find a variable given its name.
If the variable can't be found,
`Env.find` returns `None` instead of raising an exception:

[% inc file="env.py" keep="body" %]

## Visiting Nodes {: #template-nodes}

As [%x check %] explained,
HTML pages are usually stored in memory as trees
and processed using the [%i "Visitor pattern" "Visitor" %] [%i "design pattern" "pattern" %].
We therefore create a `Visitor` class
whose [%i "constructor" %] takes the root node of the [%i "DOM tree" %]
as an argument and saves it.
Calling `Visitor.walk` without a value starts [%i "recursion" %] from that saved root;
when `.walk` is given a value (as it is during recursive calls),
it uses that instead.

[% inc file="visitor.py" %]

`Visitor` defines two [%g abstract_method "abstract methods" %] `open` and `close`
that are called when we first arrive at a node and when we are finished with it.
These methods are called "abstract" because we can't actually use them:
any attempt to do so will [%i "raise" %] an [%i "exception" %],
which means [%i "child class" "child classes" %] *must* override them.
(In object-oriented terminology, this means that `Visitor` is an [%g abstract_class "abstract class" %].)
This approach is different from that of the visitor in [%x check %],
where we defined do-nothing methods so that derived classes could override
only the ones they needed.

The `Expander` class is specialization of `Visitor`
that uses an `Env` to keep track of variables.
It imports handlers for each type of special node—we will explore those in a moment—and
saves them along with a newly-created environment and a list of strings
making up the output:

<div class="pagebreak"></div>

[% inc file="expander.py" keep="construct" %]

When recursion encounters a new node,
it calls `open` to do one of three things:

1.  If the node is plain text,
    copy it to the output.

1.  If there is a handler for the node,
    call the handler's `open` or `close` method.

1.  Otherwise, open a regular [%i "tag (in HTML)" "tag" %].

[% inc file="expander.py" keep="open" %]

`Expander.close` works much the same way.
Both methods find handlers by comparing the DOM node's attributes
to the keys in the dictionary of handlers built during construction:
{: .continue}

[% inc file="expander.py" keep="handlers" %]

Finally, we need a few helper methods to show tags and generate output:
{: .continue}

[% inc file="expander.py" keep="helpers" %]

Notice that `Expander` adds strings to an array
and joins them all right at the end
rather than concatenating strings repeatedly.
Doing this is more efficient;
it also helps with debugging,
since each string in the array corresponds to a single method call.

## Implementing Handlers {: #template-handlers}

Our last task is to implement the handlers for filling in variables' values,
looping,
and so on.
We could define an [%i "abstract class" %] with `open` and `close` methods,
derive one class for each of the template expander's capabilities,
and then construct one instance of each class for `Expander` to use,
but there's a simpler way.
When Python executes the statement `import something`
it executes the file `something.py`,
saves the result in a specialized dictionary-like object,
and assigns that object to the variable `something`.
That object can also be saved in data structures like lists and dictionaries
or passed as an argument to a function
just like numbers, functions, and classes—remember,
programs are just data.

Let's write a pair of functions
that each take an expander and a node as inputs
and expand a DOM node with a `z-num` attribute
to insert a number into the output:

[% inc file="z_num.py" %]

When we enter a node like `<span z-num="123"/>`
this handler asks the expander to show an [%i "opening tag" %]
followed by the value of the `z-num` attribute.
When we exit the node,
the handler asks the expander to close the tag.
The handler doesn't know whether things are printed immediately,
added to an output list,
or something else;
it just knows that whoever called it implements the low-level operations it needs.
{: .continue}

Here's how we connect this handler (and others we're going to write in a second)
to the expander:

[% inc file="expander.py" keep="import" %]

The `HANDLERS` dictionary maps the names of special attributes in the HTML to modules,
each of which defines `open` and `close` functions for the expander to call.
In other words,
we are using modules to prevent [%i "name collision" %]
just as we would use classes or functions.

The handlers for variables are:

<div class="pagebreak"></div>

[% inc file="z_var.py" %]

This code is almost the same as the previous example.
The only difference is that instead of copying the attribute's value
directly to the output,
we use it as a key to look up a value.
{: .continue}

These two pairs of handlers look plausible, but do they work?
To find out,
we can build a program that loads variable definitions from a JSON file,
reads an HTML template using the [Beautiful Soup][beautiful_soup] module,
and does the expansion:

[% inc file="template.py" %]

We added new variables for our test cases one by one
as we were writing this chapter.
To avoid repeating text repeatedly,
here's the entire set:

[% inc file="vars.json" %]

Our first test checks whether static text is copied over as-is:

<table class="twocol">
  <tbody>
    <tr>
      <td markdown="1">[% inc file="static_text.ht" %]</td>
      <td markdown="1">[% inc file="static_text.out" %]</td>
    </tr>
  </tbody>
</table>

Good.
Now, does the expander handle constants?

<table class="twocol">
  <tbody>
    <tr>
      <td markdown="1">[% inc file="single_constant.ht" %]</td>
      <td markdown="1">[% inc file="single_constant.out" %]</td>
    </tr>
  </tbody>
</table>

What about a single variable?
{: .continue}

<table class="twocol">
  <tbody>
    <tr>
      <td markdown="1">[% inc file="single_variable.ht" %]</td>
      <td markdown="1">[% inc file="single_variable.out" %]</td>
    </tr>
  </tbody>
</table>

What about a page containing multiple variables?
There's no reason it should fail if the single-variable case works,
but we should still check—again,
software isn't done until it has been tested.

<table class="twocol">
  <tbody>
    <tr>
      <td markdown="1">[% inc file="multiple_variables.ht" %]</td>
      <td markdown="1">[% inc file="multiple_variables.out" %]</td>
    </tr>
  </tbody>
</table>

<div class="callout" markdown="1">

### Generating Element IDs

It's often handy to have a unique identifier for every element in a page,
so some templating engines automatically generate `id` attributes
for elements that don't specify IDs explicitly.
If you do this,
please do not generate random numbers,
because then Git and other version control systems will think a regenerated page has changed
when it actually hasn't.
Generating sequential IDs is equally problematic:
if you add an item to a list at the top of the page,
for example,
that might change the IDs for all of the items in subsequent (unrelated) lists.

</div>

## Control Flow {: #template-flow}

Our tool supports conditional expressions and loops.
Since we're not implementing [%g boolean_expression "Boolean expressions" %] like `and` and `or`,
all we have to do for a condition is look up a variable
and then expand the node if Python thinks the variable's value is [%g truthy "truthy" %]:

[% inc file="z_if.py" %]

Let's test it:

<table class="twocol">
  <tbody>
      <tr>
        <td markdown="1">[% inc file="conditional.ht" %]</td>
        <td markdown="1">[% inc file="conditional.out" %]</td>
      </tr>
  </tbody>
</table>

<div class="callout" markdown="1">

### Spot the Bug

This implementation of `if` contains a subtle bug.
`open` and `close` both check the value of the control variable.
If something inside the body of the `if` changes that value,
the result could be an opening tag
without a matching [%i "closing tag" %] or vice versa.
We haven't implemented an assignment operator,
so right now there's no way for that to happen,
but it's a plausible thing for us to add later,
and tracking down a bug in old code that is revealed by new code
is always a headache.

</div>

Finally we have loops.
For these,
we need to get the array we're looping over from the environment
and do the following for each item it contains:

1.  Create a new stack frame holding the current value of the loop variable.

1.  Expand all of the node's children with that stack frame in place.

1.  Pop the stack frame to get rid of the temporary variable.

[% inc file="z_loop.py" %]

Once again,
it's not done until we test it:

<table class="twocol">
  <tbody>
      <tr>
        <td markdown="1">[% inc file="loop.ht" %]</td>
        <td markdown="1">[% inc file="loop.out" %]</td>
      </tr>
  </tbody>
</table>

We have just implemented another simple programming language
like the one in [%x interp %].
It's unlikely that anyone would want to use it as-is,
but adding a new feature is now as simple as writing a matching pair
of `open` and `close` functions.

## Summary {: #template-summary}

[%f template-concept-map %] summarizes the key ideas in this chapter,
some of which we first encountered in [%x interp %].
Please see [%x bonus %] for extra material related to these ideas.

[% figure
   slug="template-concept-map"
   img="concept_map.svg"
   alt="Concept map for HTML templating"
   caption="HTML templating concept map."
   cls="here"
%]

## Exercises {: #template-exercises}

### Tracing Execution {: .exercise}

Add a directive `<span z-trace="variable"/>`
that prints the current value of a variable for debugging.

### Unit Tests {: .exercise}

Write unit tests for template expansion using [pytest][pytest].

### Sub-keys {: .exercise}

Modify the template expander so that a variable name like `person.name`
looks up the `"name"` value in a dictionary called `"person"`
in the current environment.

### Literal Text {: .exercise}

Add a directive `<div z-literal="true">…</div>` that copies the enclosed text as-is
without interpreting or expanding any contained directives.
(A directive like this would be needed when writing documentation for the template expander.)

### Including Other Files {: .exercise}

1.  Add a directive `<div z-include="filename.html"/>` that includes another file
    in the file being processed.

2.  Should included files be processed and the result copied into the including file,
    or should the text be copied in and then processed?
    What difference does it make to the way variables are evaluated?

### HTML Snippets {: .exercise}

Add a directive `<div z-snippet="variable">…</div>` that saves some text in a variable
so that it can be displayed later.
For example:

```html
<html>
  <body>
    <div z-snippet="prefix"><strong>Important:</strong></div>
    <p>Expect three items</p>
    <ul>
      <li z-loop="item:names">
        <span z-var="prefix"><span z-var="item"/>
      </li>
    </ul>
  </body>
</html>
```

would print the word "Important:" in bold before each item in the list.
{: .continue}

### YAML Headers {: .exercise}

Modify the template expander to handle variables defined in a YAML header in the page being processed.
For example, if the page is:

```html
---
name: "Dorothy Johnson Vaughan"
---
<html>
  <body>
    <p><span z-var="name"/></p>
  </body>
</html>
```

will create a paragraph containing the given name.
{: .continue}

### Expanding All Files {: .exercise}

Write a program `expand_all.py` that takes two directory names as command-line arguments
and builds a website in the second directory by expanding all of the HTML files found in the first
or in sub-directories of the first.

### Counting Loops {: .exercise}

Add a directive `<div z-index="indexName" z-limit="limitName">…</div>`
that loops from zero to the value in the variable `limitName`,
putting the current iteration index in `indexName`.

### Boolean Expression {: .exercise}

Design and implement a way to express the Boolean operators `and` and `or`.

### Element IDs {: .exercise}

The callout earlier said that
templating systems should not generate random or sequential IDs for elements.
A colleague of yours has proposed generating the IDs
by hashing the element's content,
since this will stay the same as long as the content does.
What are the pros and cons of doing this?
