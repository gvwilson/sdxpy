---
syllabus:
-   Parsing transforms text that's easy for people to read into objects that are easy for computers to work with.
-   A grammar defines the textual patterns that a parser recognizes.
-   Most parsers tokenize input text and then analyze the tokens.
-   Most parsers need to implement some form of precedence to prioritize different patterns.
-   Programs can use introspection and dynamic dispatch to inspect their own internals
    and select operations while running.
-   Operations like addition and function call work just like user-defined functions.
-   Programs can overload built-in operators by defining specially-named methods
    that are recognized by the compiler or interpreter.
status: "awaiting revision"
depends:
-   glob
---

We constructed objects to match patterns in [%x glob %],
but an [%i "expression" %] like `"2023-*{pdf,txt}"`
is a lot easier to read and write
than `Lit("2023-", Any(Either("pdf", "txt")))`.
If we want to use the former,
we need a [%g parser "parser" %]
to convert those strings to objects.

Most parsers are written in two parts ([%f parse-pipeline %]).
The first groups characters into atoms of text called "[%g token "tokens" %]".
The second assembles those tokens to create
an [%g abstract_syntax_tree "abstract syntax tree" %] (AST).

[% figure
   slug="parse-pipeline"
   img="pipeline.svg"
   alt="Parsing pipeline"
   caption="Stages in parsing pipeline."
%]

[%t parse-grammar %] shows the [%g grammar "grammar" %] our parser will handle.

<div class="table" id="parse-grammar" caption="Glob grammar." markdown="1">
| Meaning                   | Character       |
| ------------------------- | --------------- |
| Any literal character *c* | *c*             |
| Zero or more characters   | `*`             |
| Alternatives              | `{`*x*`,`*y*`}` |
</div>

When we are done,
our parser should be able to recognize that `2023-*.{pdf,txt}` means,
a literal `2023-`,
any characters,
literal `.`,
and then either a literal `pdf` or a literal `txt`.

<div class="callout" markdown="1">

### Please Don't Write Parsers

Languages that are comfortable for people to read and write
are usually difficult for computers to understand
and vice versa,
so we need parsers to translate the former into the latter.
However,
the world doesn't need more file formats:
please use [%g csv "CSV" %], [%g json "JSON" %], [%g yaml "YAML" %],
or something else that already has an acronym
rather than inventing something of your own.

</div>

## Tokenizing {: #parse-token}

A token is a meaningful piece of text,
such as the digits making up a number or the letters making up a variable name.
Our grammar's tokens are the special characters `*`, `{`, `}`, and `,`;
any sequence of one or more other characters is a single multi-letter token.
This classification guides the design of our parser:

1.  If it is a [%i "literal" %] then
    combine it with the current literal (if there is one)
    or start a new literal (if there isn't).

1.  If a character is special,
    close the existing literal (if there is one)
    and then create a token for the special character.
    Note that the `,` character closes a literal but doesn't produce a token.

The result of tokenization is a flat list of tokens.
We could pass around a list and append to it,
but we also need to know the characters in each `Lit`
and the options in each `Either`.
We will therefore create a class with state
rather than writing a function and passing state around explicitly.

The main method of our tokenizer looks like this:

[% inc file="tokenizer.py" keep="tok" %]

This method calls `self._setup()` at the start
so that the tokenizer can be re-used.
It *doesn't* call `self._add()` for regular characters;
instead,
it creates a `Lit` entry when it encounters a special character
(i.e., when the current literal ends)
and after all the input has been parsed
(to capture the last literal).

The method `self._add` adds the current thing to the list of tokens.
As a special case,
`self._add(None)` means "add the literal but nothing else"
([%f parse-tokenize %]):

[% inc file="tokenizer.py" keep="add" %]

[% figure
   slug="parse-tokenize"
   img="tokenize.svg"
   alt="Tokenizing"
   caption="Steps in tokenizing a string."
%]

Finally,
we work backward to initialize the tokenizer when we construct it
and to define the set of characters that make up literals:

[% inc file="tokenizer.py" keep="class" %]

We can now write a few tests to check that
the tokenizer is producing a list of lists
in which each sub-list represents a single token:

[% inc file="test_tokenizer.py" keep="tests" %]

## Parsing {: #parse-parse}

We now need to turn the list of tokens into a tree.
Just as we used a class for tokenizing,
we will create one for parsing
and give it a `_parse` method to start things off.
This method doesn't do any conversion.
Instead,
it takes a token off the front of the list
and figures out which method handles tokens of that kind:

[% inc file="parser.py" keep="parse" %]

<div class="callout" markdown="1">

### Introspection and Dispatch

Having a program look up a function or method inside itself
while it is running
is an example of [%g introspection "introspection" %].
Using this to decide what to do next
rather than having a long chain of `if` statements
is often called [%g dynamic_dispatch "dynamic dispatch" %],
since the code doing the lookup
(in this case, the `_parse` method)
decides who to give work to on the fly.
Introspection and dispatch are powerful techniques;
we will see a lot of them in chapters to come.

</div>

The handlers for `Any` and `Lit` are straightforward—the
hardest part is actually to make sure we name them properly
so that `_parse` can look them up:

[% inc file="parser.py" keep="simple" %]

`Either` is a little messier.
We didn't save the commas,
so we'll just pull two tokens and store those:

[% inc file="parser.py" keep="either" %]

However,
a better approach is to take tokens from the list until we see an `EitherEnd`:

[% inc file="better_parser.py" keep="either" %]

Time for some tests:

[% inc file="test_parser.py" keep="sample" %]

This test assumes we can compare `Match` objects using `==`,
just as we would compare numbers or strings.
so we add a `__eq__` method to our classes:

[% inc file="match.py" keep="equal" %]

<div class="callout" markdown="1">

### They're Just Methods

[%g operator_overloading "Operator overloading" %]
relies on the fact that when Python sees `a == b` it calls `a.__eq__(b)`.
Similarly,
`a + b` is "just" a called to `a.__add__(b)`, and so on,
so if we give our classes methods with the right names,
we can manipulates objects of those classes using familiar operations.
And yes,
this is another example of introspection.

Since we're using [%i "inheritance" %] to implement our matchers,
we write the check for equality in two parts.
The [%i "parent class" %] `Match` performs the checks that all classes need to perform
(in this case,
that the objects being compared have the same
[%g concrete_class "concrete class" %]).
If the [%i "child class" %] needs to do any more checking
(for example, that the characters in two `Lit` objects are the same)
it calls up to the parent method first,
then adds its own tests.

</div>

## Summary {: #parse-summary}

[% figure
   slug="parse-concept-map"
   img="concept_map.svg"
   alt="Concept map for parser"
   caption="Parser concept map."
%]

## Exercises {: #parse-exercises}

### Escape Characters {: .exercise}

Modify the parser to handle escape characters,
so that (for example) `\*` is interpreted as a literal '*' character
and `\\` is interpreted as a literal backslash.

### Character Sets {: .exercise}

Modify the parser so that expressions like `[xyz]` are interpreted to mean
"match any one of the characters 'x', 'y', or 'z'".
(Note that this is a shorthand for `{x,y,z}`.)

### Negation {: .exercise}

Modify the parser so that `[!abc]` is interpreted as
"none of the characters 'a', 'b', or 'c'".

### Nested Lists {: .exercise}

Write a function that accepts a string representing nested lists containing numbers
and returns the actual list.
For example, the input `[1, [2, [3, 4], 5]]`
should produce the corresponding Python list.

### Simple Arithmetic {: .exercise}

Write a function that accepts a string consisting of numbers
and the basic arithmetic operations `+`, `-`, `*`, and `/`
and produces a nested structure showing the operations
in the correct order.
For example,
`1 + 2 * 3` should produce
`["+", 1, ["*", 2, 3]]`.
