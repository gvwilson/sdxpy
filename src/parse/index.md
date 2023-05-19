---
syllabus:
-   Parsing in two or more passes is often simpler than parsing in a single pass.
-   Tokenize input text and then analyze the tokens.
---

We constructed objects to match patterns in [%x glob %].
It takes a lot less typing to write them as strings like `2023-*.{pdf,txt}`,
but if we do that we need a [%i "parser" %][%g parser "parser" %][%/i%]
to convert those strings to objects.

<div class="table" id="parser-grammar" caption="Glob grammar." markdown="1">
| Meaning                   | Character       |
| ------------------------- | --------------- |
| Any literal character *c* | *c*             |
| Zero or more characters   | `*`             |
| Alternatives              | `{`*x*`,`*y*`}` |
</div>

[%t parser-grammar %] shows the grammar our parser will handle.
When we are done,
it should be able to parse `2023-*.{pdf,txt}` as
"literal `2023-`,
any characters,
literal `.`,
either literal `pdf` or literal `txt`".

<div class="callout" markdown="1">

### Please don't write parsers

Languages that are comfortable for people to read and write
are usually difficult for computers to understand
and vice versa,
so we need parsers to translate the former into the latter.
However,
the world doesn't need more file formats:
please use CSV, JSON, [%g yaml "YAML" %],
or something else that already has an acronym
rather than inventing something of your own.

</div>

To keep our code manageable,
and to make testing easier,
we will parse in two stages ([%f parse-pipeline %]):

1.  Convert text into atoms of text (called "[%g token "tokens" %]").

2.  Assemble the tokens to generate an [%g abstract_syntax_tree "abstract syntax tree" %].

[% figure
   slug="parse-pipeline"
   img="pipeline.svg"
   alt="Parsing pipeline"
   caption="Stages in parsing pipeline."
%]

## Tokenizing {: #parser-tokenize}

A [%i "token (in parsing)" %]token[%/i%] is a meaningful piece of text,
such as the digits making up a number or the letters making up a variable name.
Our grammar's tokens are the special characters `*`, `{`, `}`, and `,`;
any sequence of one or more other characters is a single multi-letter token.
This classification guides the design of our parser:

1.  If it is a [%i "literal (in parsing)" %][%g literal "literal" %][%/i%] then
    combine it with the current literal (if there is one)
    or start a new literal (if there isn't).

1.  If a character is special,
    close the existing literal (if there is one)
    and then create a token for the special character.
    Note that the `,` character closes a literal but doesn't produce a token.

The result of tokenization is a flat list of tokens.
We could pass around a list and append to it,
but we also need to know the characters in each `Lit` and the options in each `Either`.
We will therefore create a class with state
rather than writing a function and passing state around explicitly.

The main method of our tokenizer looks like this:

[% inc file="tokenizer.py" keep="tok" %]

It calls `self._setup()` at the start so that the tokenizer can be re-used.
It *doesn't* call `self._add()` for regular characters;
instead,
it adds `Lit` entries when it encounters special characters
and after all the input has been parsed.
The method `self._add` adds the current thing to the list of tokens;
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
the tokenizer is producing a list-of-lists structure
similar to the instructions used in [%x interp %]:

[% inc file="test_tokenizer.py" keep="tests" %]

## Parsing {: #parser-parse}

We now need to turn the list of tokens into a tree.
Since we used a class for tokenizing,
we will create another one for parsing
and give it a `_parse` method to start things off:

[% inc file="parser.py" keep="parse" %]

The `_parse` method doesn't do any conversion.
Instead,
it takes a token off the front of the list
and figures out which method handles tokens of that kind:

[% inc file="parser.py" keep="parse" %]

This is another example of the [%g dispatch "dispatch" %] technique
seen in [%x interp %].
{: .continue}

The handlers for `Any` and `Lit` are straightforward:

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

This test assumes we can compare `Match` objects,
so we add a `__eq__` method to our classes:

[% inc file="match.py" keep="equal" %]

This is called operator_overloading "Operator overloading" %],
and relies on the fact that when Python sees `a == b` it calls `a.__eq__(b)`.
The Parent `Match` class performs the checks that all classes need to perform
(in this case, that the objects being compared have the same [%g concrete_class "concrete class" %]).
If the child class needs to do any more checking
(for example, that the characters in two `Lit` objects are the same)
it calls up to the parent method first,
then adds its own tests.

## Summary {: #parser-summary}

[% figure
   slug="parser-concept-map"
   img="concept_map.svg"
   alt="Concept map for parser"
   caption="Parser concept map."
%]

## Exercises {: #parser-exercises}

### Escape characters {: .exercise}

Modify the parser to handle escape characters,
so that (for example) `\*` is interpreted as a literal '*' character
and `\\` is interpreted as a literal backslash.

### Character sets {: .exercise}

Modify the parser so that expressions like `[xyz]` are interpreted to mean
"match any one of the characters 'x', 'y', or 'z'".
(Note that this is a shorthand for `{x,y,z}`.)

### Nested lists {: .exercise}

Write a function that accepts a string representing nested lists containing numbers
and returns the actual list.
For example, the input `[1, [2, [3, 4], 5]]`
should produce the corresponding Python list.
