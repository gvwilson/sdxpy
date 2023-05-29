---
syllabus:
-   An abstract syntax tree (AST) represents the elements of a program as a data structure.
-   A linter checks that a program conforms to a set of style and usage rules.
-   Linters typically use the Visitor design pattern to find nodes of interest in an AST.
-   Programs can modify a program's AST and then unparse it to create modified versions of the original program.
-   Dynamic code modification is very powerful, but the technique can produce insecure and unmaintainable code.
---

This book relies on about 2500 lines of Python to turn Markdown into HTML,
fill in cross-references,
and so on.
To keep that code readable,
we use [black][black], [flake8][flake8], and [isort][isort]
to check that lines aren't too long,
that classes and functions have consistent names,
that modules are imported in a consistent order,
and dozens of other things.

Checking tools are often called [%g linter "linters" %]
because an early tool like this for the C programming language was called `lint`.
Many projects insist that code pass checks like these
before being committed to version control.
To show how they work,
this chapter builds a trio of simple linting tools
that find duplicate keys in dictionaries,
look for unused variables,
and create a table showing which classes in a hierarchy define which methods.
As a bonus,
we then show how these tools can be used to extract documentation
and to create code as well as check it.

## Machinery {: #linter-machinery}

Our starting point is Python's [ast][py_ast] module,
which parses Python code and produces an [%g abstract_syntax_tree "abstract syntax tree" %]
that represents the structure of the code.
For example,
suppose we have this short program:

[% inc file="simple.py" %]

[%f linter-ast-simple %] shows the main parts of this program's AST.
Each node represents one element of the program,
and each node's children are the element nested within it.
{: .continue}

[% figure
   slug="linter-ast-simple"
   img="ast_simple.svg"
   alt="Simple AST"
   caption="The abstract syntax tree for a simple Python program."
%]

We say "main parts of the AST" because
the full structure includes placeholders for elements
that aren't present in this program.
To see the full thing,
we can use `ast.parse` to turn our short program into an AST
and `ast.dump` to display it:

[% inc file="dump_ast.py" %]
[% inc pat="dump_ast_simple.*" fill="sh out" %]

Looking at the node representing the definition of the function `double`,
it has:
{: .continue}

-   a `name`;
-   an `arguments` node that stores information about the function's arguments;
-   a `body` that holds a list of the statements making up the function; and
-   a list of decorators applied to the function (which is empty).

If we want a list of all the functions defined in this module,
we can walk through this tree to find all the `FunctionDef` nodes
and record their `name` properties.
Since each node's structure is a little different,
we would have to write one function for each type of node
that knew which fields of that node were worth exploring.

Luckily for us,
the [ast][py_ast] module comes with tools that can do this for us.
The class `ast.NodeVisitor` uses
the [%i "Visitor pattern" "design pattern!Visitor" %][%g visitor_pattern "Visitor" %][%/i%] design pattern
to recurse through an AST.
Each time it reaches a new node of type `Thing`,
it looks for a method called `visit_Thing`;
for example,
when it reaches a `FunctionDef` node it looks for `visit_FunctionDef`.
If that method has been defined,
`NodeVisitor` calls it with the node as an argument.
The class `CollectNames` uses this machinery
to create a list of all the function and variable names
defined in a program:

[% inc file="walk_ast.py" keep="class" %]

A few things worth noting about this class are:
{: .continue}

1.  The constructor of `CollectNames` invokes
    the constructor of `NodeVisitor`
    using `super().__init__()`
    before doing anything else.

1.  The methods `visit_Assign` and `visit_FunctionDef`
    must call `self.generic_visit(node)` explicitly
    to recurse down through their children.
    By requiring this to be explicit,
    `NodeVisitor` gives programmers control on whether and when recursion takes place.

1.  The method `position` relies on the fact that
    every node in the ATS keeps track of
    where in the source code it came from.

To use this class,
we read in a source program that we want to analyze,
parse it,
and then call the `visit` method of our class to trigger recursion:

[% inc file="walk_ast.py" keep="main" %]

Here's its output for our simple test program:

[% inc pat="walk_ast.*" fill="sh out" %]

With a little more work we could record class names as well,
and then check that (for example)
class names use CamelCase
while function and variable names use pothole\_case.
We'll tackle this in the exercises.

## Finding Things {: #linter-find}

Many programs store their configuration in dictionaries.
As those dictionaries grow larger,
it's easy for programmer to redefine values by accident.
Python doesn't consider this an error—for example,
both `no_duplicates` and `has_duplicates` are valid two-element dictionaries:

[% inc file="has_duplicate_keys.py" %]

<div class="callout" markdown="1">

### Overwriting, not Appending

Programmers who are new to Python sometimes believe that
the "extra" values in the dictionary `has_duplicates`
should be put in a list,
so that (for example) the key `"third"` has the value `[3, 6]`.
This behavior would be perfectly reasonable,
but it isn't what Python does.

</div>

We can built a linter that finds dictionaries like `has_duplicates`
in just 17 lines of code.
We define a `visit_Dict` method for `NodeVisitor` to call;
in it,
we add each constant key to an instance of `Counter`
(a specialized `dict` that counts entries`)
and then look for keys that have been seen more than once:

[% inc file="find_duplicate_keys.py" keep="class" %]

Its output for the file containing our two example dictionaries is:
{: .continue}

[% inc file="find_duplicate_keys.out" %]

<div class="callout" markdown="1">

### As Far as We Can Go

`FindDuplicateKeys` only considers constant keys,
so it won't find duplicate keys that are created on the fly:

[% inc file="function_keys.py" %]

We could try adding logic to handle this,
but one of the fundamental theorems of computer science is that
it's impossible to create a program that can predict the output of arbitrary other programs.
Our linter can therefore produce [%g false_negative "false negatives" %],
i.e.,
tell us there aren't problems when there actually are.

</div>

Finding unused variables—ones that are assigned values but never used—is
more challenging than our previous examples.
The problem is [%g scope "scope" %]:
a variable defined in a function or method might have the same name
as one defined elsewhere,
but they are different variables.

Let's start by defining a class that handles modules and functions.
Since functions can be defined inside modules,
and inside other functions,
our class's constructor creates a list that we will use as a stack
to keep track of what scopes we're currently in:

[% inc file="find_unused_variables.py" keep="class" %]

Each time we encounter a new scope
we push a triple onto the stack with a name,
a set to hold the variables that are used in the scope,
and another set to hold the variables that are defined in the scope.
We then call `NodeVisitor.generic_visitor` to trigger recursion,
pop the record we just pushed off the stack,
and report any problems:

[% inc file="find_unused_variables.py" keep="search" %]

We could just use a list of three values to record information for each scope,
but it's a little cleaner to use `namedtuple`
from Python's standard library:

[% inc file="find_unused_variables.py" keep="scope" %]

The last part of the puzzle is `visit_Name`.
If the variable's value is being read,
the node will have a property `.ctx` (short for "context") of type `Load`.
If the variable is being written to,
the node's `.ctx` property will be an instance of `Store`.
Checking this property allows us to put the name in the right set
in the scope that's at the top of the stack:

[% inc file="find_unused_variables.py" keep="name" %]

Once again,
we can run this by reading the source of a program,
converting it to an AST,
constructing an instance of `FindUnusedVariables`,
and running its `visit` method:

[% inc file="find_unused_variables.py" keep="main" %]

To test our code,
let's create a program that has some unused variables:

[% inc file="has_unused_variables.py" %]

When we run our linter we get:

[% inc file="find_unused_variables.out" %]

For our last example of finding things,
let's build a tool that tells us which methods are defined in which classes.
(We used a tool like this when writing this book
to keep track of examples that evolved step by step.)
Here's a test file that defines four classes,
each of which defines or redefines some methods:

[% inc file="inheritance_example.py" %]

As before,
our class's constructor creates a stack to keep track of where we are.
It also creates a couple of dictionaries to keep track of
how classes inherit from each other
and the methods each class defines:

[% inc file="inheritance.py" keep="init" %]

When we encounter a new class definition,
we push its name on the stack,
record its parents,
and create an empty set to hold its methods:

[% inc file="inheritance.py" keep="classdef" %]

When we encounter a function definition,
the first thing we do is check the stack.
If it's empty,
we're looking at a top-level function rather than a method,
so there's nothing for us to do.
(We actually should recurse through the function's children,
since it's possible to define classes inside functions,
but we'll leave as an exercise.)
If this function definition is inside a class,
on the other hand,
we add its name to our records:

[% inc file="inheritance.py" keep="methoddef" %]

Once we're done searching the AST we print out a table
of the classes and methods we've seen ([%t linter-inheritance %]).
We could make this display easier to read—for example,
we could sort the classes from parent to child
and display methods in the order in which they were first defined—but
none of that requires us to inspect the AST.

<div class="table" id="linter-inheritance" caption="Inheritance and methods" markdown="1">
| | GrandChild | LeftChild | Parent | RightChild |
| --- | --- | --- | --- | --- |
| blue | X | X |   | X
| green |   | X | X |
| orange | X |   |   |
| red | X |   | X | X
</div>

## Extension {: #linter-extension}

It's easy to check a single style rule by extending `NodeVisitor`,
but what if we want to check dozens of rules?
Traversing the AST dozens of times would be inefficient.
And what if we want people to be able to add their own rules?
Inheritance is the wrong tool for this:
if several people each create their own `NodeVisitor` with a `visit_Name` method,
we'd have to inherit from all those classes
and then have the new class's `visit_Name` call up to all of its parents' equivalent methods.

One way around this is to [%g method_injection "inject" %] methods into classes
after they have been defined.
The code fragment below creates a new class called `BlankNodeVisitor`
that doesn't add anything to `NodeVisitor`,
then uses `setattr` to add a method to it after it has been defined:

[% inc file="injection.py" keep="attach" %]

This trick works because classes and objects are just specialized dictionaries
(for some large value of "just").
If we create an object of `BlankNodeVisitor` and call its `visit` method:

[% inc file="injection.py" keep="main" %]

then the inherited `generic_visit` method does what it always does.
When it encounters a `Name` node,
it looks in the object for something called `visit_Name`.
Since it doesn't find anything,
it looks in the object's class for something with that name,
finds our injected method,
and calls it.

With a bit more work we could have our injected method save and then call
whatever `visit_Name` method was there when it was added to the class,
but we would quickly run into a problem.
As we've seen in earlier examples,
the methods that handle nodes are responsible for deciding
whether and when to recurse into those nodes' children.
If we pile method on top of one another,
then either each one is going to trigger recursion
(so we recurse many times)
or there will have to be some way for each one to signal
whether it did that
so that other methods don't.

To avoid this complication,
most systems use a different approach.
Consider this class:

[% inc file="register.py" keep="class" %]

The `add_handler` method takes three parameters:
the type of node a callback function is meant to handle,
the function itself,
and an optional extra piece of data to pass to the function
along with an AST node.
It saves the handler function and the data in a lookup table
indexed by the type of node the function is meant to handle.
Each of the methods inherited from `NodeVisitor`
then looks up handlers for its node type and runs them.

So what do handlers look like?
Each one is a function that takes a node and some data as input
and does whatever it's supposed to do:

[% inc file="register.py" keep="handler" %]

Setting up the visitor is a bit more complicated,
since we have to create and register the handler:

[% inc file="register.py" keep="main" %]

However,
we can now register as many handlers as we want
for each kind of node.
{: .continue}

## Generating Documentation {: #linter-docs}

Many programmers believe they're more likely to write documentation and keep it up to date
if it is close to the code.
Tools that extract specially-formatted comments from code and turn them into documentation
have been around since at least the 1980s;
both [Sphinx][sphinx] and [MkDocs][mkdocs] are popular ones for Python.

Generating documentation isn't the same as checking code style,
but they share some tooling.
Let's start by building a `NodeVisitor` that extracts and saves docstrings:

[% inc file="doc_extract.py" keep="start" %]

The code to create a stack,
extract docstrings,
and save them in a dictionary should look familiar by now:

[% inc file="doc_extract.py" keep="body" %]

To format the docstrings,
we create a Markdown page with module, class, and function names as headers:

[% inc file="doc_format.py" keep="format" %]

If our input file looks like this:

[% inc file="doc_sample.py" %]

then our output is:
{: .continue}

[% inc file="doc_sample.out" %]

## Modifying Code {: #codegen-modify}

An AST is a data structure like any other,
which means we can modify it as well as inspecting it.
Let's start with this short program:

[% inc file="double_and_print.py" %]

Its AST has two top-level nodes:
one for the function definition and one for the `print` statement.
We can duplicate the second of these and then [%g unparsing "unparse" %] the AST
to produce a new program:

[% inc file="unparse.py" keep="modify" %]
[% inc file="unparse_modified.out" %]

To run our machine-generated program,
we have to compile the AST to [%g bytecode "bytecode" %]
and tell Python to evaluate the result:

[% inc file="unparse.py" keep="exec" %]
[% inc file="unparse_exec.out" %]

Duplicating a `print` statement isn't particularly useful,
but other applications of this technique let us do some powerful things.
Let's have another look at how Python represents a function call.
Our example is:

[% inc file="call.py" %]

We parse it like this:
{: .continue}

[% inc file="inject.py" keep="parse" %]

and get this AST:
{: .continue}

[% inc file="inject_parse.out" %]

But we don't have to parse text to create an AST:
it's just a bunch of objects,
so we can construct one by hand
that mirrors the structure shown above:

[% inc file="inject.py" keep="make" %]
[% inc file="inject_make.out" %]

Alternatively,
we can find existing function definitions
and modify them programmatically:

[% inc file="inject.py" keep="modify" %]

To try this out,
here's a program that adds and doubles numbers:

[% inc file="add_double.py" %]

The modified version is:
{: .continue}

[% inc file="inject_modified.out" %]

So what exactly is `call`?
We want a "function" that keeps track of
how many times it has been passed different strings,
so we define a class with a `__call__` method
so that its instances can be used like functions:

[% inc file="inject.py" keep="counter" %]

Finally,
when we're evaluating the bytecode generated from our modified AST,
we pass in a dictionary of variable names and values
that we want to have in scope.
The result is exactly what we would get if we had defined all of this in the usual way:

[% inc file="inject.py" keep="exec" %]
[% inc file="inject_exec.out" %]

<div class="callout" markdown="1">

### There's Such a Thing as "Too Clever"

Modifying code dynamically is the most powerful technique shown in this book.
It is also the least comprehensible:
as soon as the code you read and the code that's run can differ in arbitrary ways,
you have a maintenance headache and a security nightmare.
Limited forms of program modification,
such as Python's [metaclasses][py_metaclass] or [%g decorator "decorators" %]
give most of the power with only some of the headaches;
please use those rather than the magic shown above.

</div>

## Summary {: #linter-summary}

[% figure
   slug="linter-concept-map"
   img="concept_map.svg"
   alt="Concept map for code manipulation"
   caption="Concepts for code manipulation."
%]

## Exercises {: #linter-exercises}

### Finding unused parameters {: .exercise}

Modify the code that finds unused variables
to report unused function parameters as well.

### Finding redundant assignments {: .exercise}

Write a linter that looks for redundant assignments to variables,
i.e.,
assignments that are immediately overwritten:

```python
x = 1  # redundant
x = 2
```

(Redundant assignments are a common result of copying and pasting.)
{: .continue}

### Checking names {: .exercise}

Write a linter that checks that
class names are written in CamelCase
but function and variable names are pothole\_case.

### Missing documentation {: .exercise}

Write a linter that complains about modules, classes, methods, and functions
that don't have docstrings.

### Missing tests {: .exercise}

Write a linter that takes two files as input:
one that defines one or more functions
and another that defines one or more tests of those functions.
The linter looks through the tests to see what functions are being called,
then reports any functions from the first file that it hasn't seen.

### Nested functions {: .exercise}

Modify the inheritance table code
so that class names are shown in parent-to-child order
and methods are shown in the order in which they are first defined.
(You may find the discussion of
[%i "topological order" %][%g topological_order "topological ordering" %][%/i%]
in [%x build %] useful.)

### Chaining methods {: .exercise}

1.  Modify the code that injects methods into `NodeVisitor`
    so that any previously-injected methods are also called.

1.  Modify the methods again so that each one signals
    whether or not it has handled recursion
    (either directly or indirectly).

### Decorating {: .exercise}

Create a `@count` decorator that causes a function to count
how many times it has been called.

### Name conversion {: .exercise}

Write a tool that find functions with pothole\_case names
and replaces them with CamelCase names,
then saves the resulting program as a legal Python file.

### Sorting imports {: .exercise}

[isort][isort] checks that the imports in a file are sorted correctly:
modules from Python's standard library come first (in alphabetical order),
then installed modules (also in alphabetical order)
and finally local imports (ditto).
Write a linter that reports violations of these rules.
How did you distinguish between the three cases?
