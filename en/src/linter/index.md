---
title: "A Style Checker"
syllabus:
- FIXME
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

These tools are often called [%g linter "linters" %]
(because an early tool like this for the C programming language was called `lint`),
and many projects insist that code pass their tests
before being committed to version control.
In order to show how they work,
this chapter builds a trio of simple linting tools
that find duplicate keys in dictionaries,
look for unused variables,
and create a table showing which classes in a hierarchy define which methods.

## Machinery {: #linter-machinery}

Our starting point is Python's [ast][py_ast],
which parses Python code and produces
a data structure that represents the structure of the code
called an [%g abstract_syntax_tree "abstract syntax tree" %].
For example,
suppose we have this short program:

[% inc file="simple.py" %]

[%fixme linter-ast-simple %] shows the main parts of this program's AST.
Each node represents one element of the program,
and each node's children are the element nested within it.
{: .continue}

[% fixme
   slug="linter-ast-simple"
   img="linter-ast-simple.svg"
   alt="Simple AST"
   caption="The abstract syntax tree for a simple Python program."
%]

We say "main parts of the AST" because
the full structure includes placeholders for elements
that aren't present in this program.
To see the full thing,
we can use `ast.parse` to turn source code into a tree
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
we'd have to write one function for each type of node
that knew which fields of that node were worth exploring.

Luckily for us,
the [ast][py_ast] module comes with tools that can do this for us.
The class `ast.NodeVisitor` knows how to recurse through an AST.
Each time it reaches a new node of type `Thing`,
it looks for a method called `visit_Thing`,
e.g.,
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
    must call explicitly `self.generic_visit(node)` explicitly
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

Many programs store their configuration in dictionaries ([%x pipeline %]).
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

A linter that finds dictionaries like `has_duplicates`
is straightforward to build.
We define a `visit_Dict` method for `NodeVisitor` to call;
in it,
we add each constant key to a `Counter`
(a specialized `dict` that counts entries`)
and then look for keys that have been seen more than once.
The whole thing is just 17 lines long:

[% inc file="find_duplicate_keys.py" keep="class" %]

Its output for the file containing our two example dictionaries is:
{: .continue}

[% inc file="has_duplicate_keys_ast.out" %]

<div class="callout" markdown="1">

### As Far as We Can Go

`FindDuplicateKeys` won't actually find all duplicate dictionary keys.
To see why not, consider this:

[% inc file="function_keys.py" %]

`FindDuplicateKeys` only consider constant keys,
not keys that are created by calling functions,
concatenating strings,
and so on.
We could try adding logic to look for these,
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
| blue | X | X |   | X
| green |   | X | X |
| orange | X |   |   |
| red | X |   | X | X
</div>

## Extension {: #linter-extension}

- `injection.py` to show that we can add handlers
  - but what if we want to add lots?

- `register.py` uses a generic mechanism
  - have to create our own visitor with overrides for all the methods
  - but then we can add as much as we want

## Exercises {: #linter-exercises}

FIXME

find unused parameters as well as unused variables

check that class names are CamelCase but functions and variable are pothole\_case
