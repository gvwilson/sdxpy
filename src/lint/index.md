---
syllabus:
-   A linter checks that a program conforms to a set of style and usage rules.
-   Linters typically use the Visitor design pattern to find nodes of interest in an abstract syntax tree.
-   Programs can modify a program's AST and then unparse it to create modified versions of the original program.
-   Dynamic code modification is very powerful, but the technique can produce insecure and unmaintainable code.
depends:
-   check
status: "revised 2023-08-04"
---

This book relies on about 1800 lines of Python to turn Markdown into HTML,
fill in cross-references,
and so on.
To keep that code readable,
we use [black][black], [flake8][flake8], and [isort][isort]
to check that lines aren't too long,
that classes and functions have consistent names,
that modules are imported in a consistent order,
and dozens of other things.

Checking tools are often called [%g linter "linters" %]
because an early tool like this that found fluff in C programs was called `lint`.
Many projects insist that code pass linting checks
before being committed to version control.
To show how linters work,
this chapter builds a trio of tools that
find duplicate keys in dictionaries,
look for unused variables,
and create a table showing which classes in a hierarchy define which methods.

## Machinery {: #lint-machinery}

[%x check %] represented HTML as a [%i "DOM tree" %].
We can also represent the structure of a program
as an [%i "abstract syntax tree" %] (AST)
whose nodes represent functions,
statements,
variables,
array indexing operations,
and so on.

Python's [ast][py_ast] module will parse Python source code
and produce an AST for us.
For example,
[%f lint-ast-simple %] shows key parts of the AST
for the short program shown below:

[% inc file="simple.py" %]

[% figure
   slug="lint-ast-simple"
   img="ast_simple.svg"
   alt="Simple AST"
   caption="The abstract syntax tree for a simple Python program."
%]

We said "key parts of the AST" because
the complete structure contains many details that we haven't bothered to draw.
To see them,
let's use `ast.parse` to turn our example code into an AST
and `ast.dump` to display it:

[% inc file="dump_ast.py" %]
[% inc file="dump_ast_simple.sh" %]
[% inc file="dump_ast_simple.out" head="10" %]

The node representing the definition of the function `double`
is a `FunctionDef` node with a `name`
and an `arguments` sub-node that stores information
about the function's [%i "argument" "arguments" %];
other nodes that we have left out
represent its return value,
the call to `double`,
the assignment to `result,
and so on.

If we want a list of all the functions defined in this module,
we can walk through this tree to find all the `FunctionDef` nodes
and record their `name` properties.
Since each node's structure is a little different,
we would have to write one function for each type of node
that knew which fields of that node were worth exploring.

Luckily for us the ast module has tools to do this for us.
The class `ast.NodeVisitor` uses
the now-familiar [%i "Visitor pattern" "Visitor" %] [%i "design pattern" %]
to recurse through a structure like the one in [%f lint-ast-simple %].
Each time the visitor reaches a node of type `Thing`,
it looks for a [%i "method" %] called `visit_Thing`;
for example,
when it reaches a `FunctionDef` node it looks for `visit_FunctionDef`.
If that method has been defined,
`NodeVisitor` calls it with the node as an argument.
The class `CollectNames` uses this machinery
to create a list of the function and variable names
defined in a program:

[% inc file="walk_ast.py" keep="class" %]

A few things worth noting about this class are:
{: .continue}

1.  The [%i "constructor" %] of `CollectNames` invokes
    the constructor of `NodeVisitor`
    using `super().__init__()`
    before doing anything else.

1.  The methods `visit_Assign` and `visit_FunctionDef`
    must call `self.generic_visit(node)` explicitly
    to recurse down through their children.
    By requiring this to be explicit,
    `NodeVisitor` gives programmers control on
    whether and when [%i "recursion" %] takes place.

1.  The method `position` relies on the fact that
    every node in the AST keeps track of
    where in the source code it came from.

To use this class,
we read the source of the program that we want to analyze,
parse it,
and then call the `visit` method of our class to trigger recursion:

[% inc file="walk_ast.py" keep="main" %]
[% inc pat="walk_ast.*" fill="sh out" %]

With a little more work we could record class names as well,
and then check that (for example)
class names use CamelCase
while function and variable names use pothole\_case.
We'll tackle this in the exercises.

## Finding Duplicate Keys {: #lint-dup}

Many programs store their configuration in dictionaries.
As those dictionaries grow larger,
it's easy for programmer to redefine values by accident.
For example,
the dictionary in this short piece of code has two entries
for the key `"third"`:

[% inc file="has_duplicate_keys.py" %]

Python could treat this as an error,
keep the first entry,
keep the last entry,
or concatenate the entries somehow.
As the output below shows,
it chooses the third option:
{: .continue}

[% inc file="has_duplicate_keys.out" %]

We can built a linter that finds dictionaries like `has_duplicates`
with just a few lines of code
and the `Counter` class from Python's [collections][py_collections] module
(which implements a specialized dictionary that counts
how many times a key has been seen).
We define a `visit_Dict` method for `NodeVisitor` 
that adds each constant key to the counter,
then look for keys that have been seen more than once:

[% inc file="find_duplicate_keys.py" keep="class" %]

Its output for the file containing our two example dictionaries is:
{: .continue}

[% inc file="find_duplicate_keys.out" %]

<div class="callout" markdown="1">

### As Far as We Can Go

`FindDuplicateKeys` only considers constant keys,
which means it won't find duplicate keys that are created on the fly like this:

[% inc file="function_keys.py" %]

We could try adding more code to handle this,
but there are so many different ways to generate keys on the fly
that our linter couldn't possibly catch them all.
The possibility of [%g false_negative "false negatives" %] doesn't mean that
linting is useless, though:
every problem that linting catches
gives programmers more time to check for things that linters can't find.

</div>

## Finding Unused Variables {: #lint-unused}

Finding unused variables—ones that are assigned values but never used—is
more challenging than our previous examples.
The problem is [%i "scope" %]:
a variable defined in a function or method might have the same name
as one defined elsewhere,
but they are different variables.

Let's start by defining a class
that handles variables in [%i "module" "modules" %] and functions.
Since functions can be defined inside modules and other functions,
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
(which also comes from Python's collections module):

[% inc file="find_unused_variables.py" keep="scope" %]

The last part of the puzzle is `visit_Name`.
If the variable's value is being read,
the node will have a property `.ctx` (short for "context") of type `ast.Load`.
If the variable is being written to,
the node's `.ctx` property will be an instance of `ast.Store`.
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

## Summary {: #lint-summary}

*Please see [%x bonus %] for extra material related to these ideas.*

[% figure
   slug="lint-concept-map"
   img="concept_map.svg"
   alt="Concept map for code manipulation"
   caption="Concepts for code manipulation."
   cls="here"
%]

## Exercises {: #lint-exercises}

### Finding Unused Parameters {: .exercise}

Modify the code that finds unused variables
to report unused function parameters as well.

### Finding Redundant Assignments {: .exercise}

Write a linter that looks for redundant assignments to variables,
i.e.,
assignments that are immediately overwritten:

```python
x = 1  # redundant
x = 2
```

(Redundant assignments are a common result of copying and pasting.)
{: .continue}

### Checking Names {: .exercise}

Write a linter that checks that
class names are written in CamelCase
but function and variable names are pothole\_case.

### Missing Documentation {: .exercise}

Write a linter that complains about modules, classes, methods, and functions
that don't have docstrings.

### Missing Tests {: .exercise}

Write a linter that takes two files as input:
one that defines one or more functions
and another that defines one or more tests of those functions.
The linter looks through the tests to see what functions are being called,
then reports any functions from the first file that it hasn't seen.

### Chaining Methods {: .exercise}

1.  Modify the code that injects methods into `NodeVisitor`
    so that any previously-injected methods are also called.

1.  Modify the methods again so that each one signals
    whether or not it has handled recursion
    (either directly or indirectly).

### Sorting Imports {: .exercise}

[isort][isort] checks that the imports in a file are sorted correctly:
modules from [%i "Python standard library" "Python's standard library" %]
come first (in alphabetical order),
then installed modules (also in alphabetical order)
and finally local imports (ditto).
Write a linter that reports violations of these rules.
How did you distinguish between the three cases?
