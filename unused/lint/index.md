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

## Exercises

### Name Conversion {: .exercise}

Write a tool that find functions with pothole\_case names
and replaces them with CamelCase names,
then saves the resulting program as a legal Python file.
