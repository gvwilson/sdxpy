---
title: "Parsing Text"
syllabus:
-   Use existing file formats rather than creating new ones.
-   Parsing in two or more passes is often simpler than parsing in a single pass.
-   Tokenize input text and then analyze the tokens.
-   Every formal language corresponds to an abstract machine and vice versa.
---

We constructed objects to create regular expressions in [%x matching %].
It takes a lot less typing to write them as strings,
but if we do that we need a [%i "parser" %][%g parser "parser" %][%/i%]
to convert those strings to objects.

<div class="table" id="parser-grammar" caption="Regular expression grammar." markdown="1">
| Meaning                   | Character |
| ------------------------- | --------- |
| Any literal character *c* | *c*       |
| Beginning of input        | ^         |
| End of input              | $         |
| Zero or more of something | \*        |
| Either/or                 | \|        |
| Grouping                  | (…)       |
</div>

[%t parser-grammar %] shows the grammar our parser will handle.
When our parser is done
it should be able to parse `^(a|b|$)*z$` as
"start of text",
"any number of 'a', 'b', or '$'",
"a single 'z',
and "end of text".
To keep our discussion focused on parsing
we will create a tree of objects ([%f parser-expression-tree %])
rather than instances of the regular expression classes from [%x matching %];
the exercises will tackle the problem of converting the former to the latter.

[% figure
   slug="parser-expression-tree"
   img="parser_expression_tree.svg"
   alt="Expression tree for regular expression"
   caption="Representing the result of parsing a regular expression as an tree."
%]

<div class="callout" markdown="1">

### Please don't write parsers

Languages that are comfortable for people to read and write
are usually difficult for computers to understand
and vice versa,
so we need parsers to translate the former into the latter.
However,
the world doesn't need more file formats:
if you need a configuration file or lookup table,
please use CSV, JSON, [%g yaml "YAML" %],
or something else that already has an acronym
rather than inventing something of your own.

</div>

## Tokenization {: #parser-tokenize}

A [%i "token (in parsing)" %][%g token "token" %][%/i%] is an atom of text,
such as the digits making up a number or the letters making up a variable name.
Our grammar's tokens are the special characters `*`, `|`, `(`, `)`, `^`, and `$`;
any sequence of one or more other characters is a single multi-letter token.
This classification guides the design of our parser:

1.  If a character is special, create a token for it.

1.  If it is a [%i "literal (in parsing)" %][%g literal "literal" %][%/i%] then
    combine it with the current literal if there is one
    or start a new literal.

1.  Since `^` and `$` are either special or regular depending on position,
    we must treat them as separate tokens or as part of a literal
    based on where they appear.

We can translate these rules almost directly into code
to create a list of dictionaries whose keys are `"kind"` and `"loc"` (short for location),
with the extra key `"value"` for literal values:

[% inc file="tokenizer_collapse.py" omit="combine" %]

The helper function `combine_or_push` does exactly what its name says.
If the thing most recently added to the list of tokens isn't a literal,
the new character becomes a new token;
otherwise,
it appends the new character to the literal:

[% inc file="tokenizer_collapse.py" keep="combine" %]

We can try this out with a three-line test program:

[% inc pat="tokenizer_collapse_example.*" fill="py out" %]

This simple tokenizer is readable, efficient, and wrong.
The problem is that the expression `ab*` is supposed to mean
"a single `a` followed by zero or more `b`".
If we combine the letters `a` and `b` as we read them,
though,
we wind up with "zero or more repetitions of `ab`".
In jargon terms,
our parser is [%i "greedy algorithm" "algorithm!greedy" %][%g greedy_algorithm "greedy" %][%/i%],
but we need it to be [%i "lazy algorithm" "algorithm!lazy" %][%g lazy_matching "lazy" %][%/i%]:

[% inc pat="tokenizer_collapse_error.*" fill="py out" %]

The solution is to treat each regular character as its own literal in this stage
and combine them later.

[% inc file="tokenizer.py" keep="tokenize" %]

Software isn't done until it's tested,
so let's build some tests.
The listing below shows a few of these
along with the output for the full set:

[% inc file="test_tokenizer.py" omit="omit" %]
[% inc file="test_tokenizer.out" %]

## Assembling the Tree {: #parser-tree}

We now have a list of tokens,
but we need a tree that represents the nesting introduced by parentheses
and the way that `*` applies to whatever comes before it.
Let's trace a few cases:

1.  If the regular expression is `a`,
    we create a `Lit` token for the letter `"a"`.

1.  If the regular expression is `a*`,
    we create a `Lit` token for the `"a"` and append it to the output list.
    When we see the `*`,
    we take that `Lit` token off the tail of the output list
    and replace it with an `Any` token that has the `Lit` token as its child.

1.  What about the regular expression `(ab)`?
    We don't know how long the group is going to be when we see the opening `(`,
    so we add the parenthesis to the output as a marker.
    We then add the `Lit` tokens for the `"a"` and `"b"` until we see the `)`,
    at which point we pull tokens off the end of the output list
    until we get back to the `(` marker.
    When we find it,
    we put everything we have temporarily collected into a `Group` token and append it to the output list.
    This algorithm automatically handles patterns like `(a*)` and `(a(b*)c)`.

1.  What about `a|b`?
    We append a `Lit` token for `"a"`, get the `|` and—we're stuck,
    because we don't yet have the next token we need to finish building the `Alt`.

One way to solve this problem is to check to see if the thing on the top of the stack is combinable
each time we append a new token.
However,
that still doesn't handle `a|b*` properly:
the pattern is supposed to mean "one `"a"` or any number of `"b"`",
but the check-and-combine strategy will turn it into the equivalent of `(a|b)*`.

A better solution is to leave some partially-completed tokens in the output
and compress them later ([%f parser-mechanics %]).
If our input is `a|b` we can:

1.  Append a `Lit` token for `"a"`.

1.  When we see `|`,
    make that `Lit` token the left child of the `Alt`
    and append that to the output without filling in the right child.

1.  Append the `Lit` token for `"b"`.

1.  After all tokens have been handled,
    look for partially-completed `Alt` tokens and make whatever comes after them their right child.

Again, this automatically handles patterns like `(ab)|c*|(de)`.
{: .continue}

[% figure
   slug="parser-mechanics"
   img="parser_mechanics.svg"
   alt="Mechanics of combining tokens"
   caption="Mechanics of combining tokens while parsing regular expressions."
%]

Let's turn this idea into code.
The main structure of our parser is:

[% inc file="parser.py" omit="skip" %]

We handle tokens case by case
(with a few assertions to check that patterns are [%g well_formed "well formed" %]):

[% inc file="parser.py" keep="handle" %]

When we find the `)` that marks the end of a group,
we take items from the end of the output list
until we find the matching start
and use them to create a group:

[% inc file="parser.py" keep="groupend" %]

Finally,
when we have finished with the input,
we go through the output list one last time to fill in the right side of `Alt`s:

[% inc file="parser.py" keep="compress" %]

Once again,
it's not done until we've tested it:

[% inc file="test_parser.py" omit="omit" %]
[% inc file="test_parser.out" %]

Our tokenizer and parser are doing some complex things,
but are still less than 100 lines of code.
Compared to parsers for formats like JSON and YAML,
though,
they are still quite simple.
If we have more operators with different
[%i "operator precedence!implementing" %][%g precedence "precedences" %][%/i%]
we should switch to the
[%i "shunting-yard algorithm" "parser!shunting-yard algorithm" %][shunting-yard algorithm][shunting_yard_algorithm][%/i%],
and if we need to parse something as complex as Python
we should explore tools like [%i "ANTLR" %][ANTLR][antlr][%/i%]
that can generate a parser automatically from a description of the language to be parsed.
As we said at the start,
though,
if our design requires us to write a parser we should come up with a better design.

<div class="callout" markdown="1">

### The limits of computing

One of the most important theoretical results in computer science is that
every formal language corresponds to a type of abstract machine and vice versa,
and that some languages (or machines) are more or less powerful than others.
For example,
every regular expression corresponds to
a [%i "finite state machine!correspondence with regular expressions" %][%g fsm "finite state machine" %][%/i%] (FSM)
like the one in [%f parser-fsm %].
As powerful as FSMs are,
they cannot match things like nested parentheses or HTML tags;
[%i "sin!using regular expressions to parse HTML" %][attempting to do so is a sin][stack_overflow_html_regex][%/i%].
If you add a stack to the system you can process a much richer set of languages,
and if you add two stacks you have something equivalent to a [%i "Turing Machine" %][%g turing_machine "Turing Machine" %][%/i%]
that can do any conceivable computation.
[% b Conery2021 %] is a good introduction to this idea
(and others)
for self-taught developers.

</div>

[% figure
   slug="parser-fsm"
   img="parser_fsm.svg"
   alt="Finite state machine"
   caption="A finite state machine equivalent to a regular expression."
%]

## Summary {: #parser-summary}

[% figure
   slug="parser-concept-map"
   img="parser_concept_map.svg"
   alt="Concept map for parser"
   caption="Parser concept map."
%]

## Exercises {: #parser-exercises}

### Create objects {: .exercise}

Modify the parser to return instances of classes derived from
the `RegexBase` class of [%x matching %].

### Escape characters {: .exercise}

Modify the parser to handle escape characters,
so that (for example) `\*` is interpreted as a literal '*' character
and `\\` is interpreted as a literal backslash.

### Lazy matching {: .exercise}

Modify the parser so that `*?` is interpreted as a single token
meaning "lazy match zero or more".

### Character sets {: .exercise}

Modify the parser so that expressions like `[xyz]` are interpreted to mean
"match any one of the characters 'x', 'y', or 'z'".

### Back reference {: .exercise}

Modify the tokenizer so that it recognizes `\1`, `\2`, and so on to mean "back reference".
The number may contain any number of digits.

### Tokenize HTML {: .exercise}

1.  Write a tokenizer for a subset of HTML that consists of:

    -   Opening tags without attributes, such as `<div>` and `<p>`
    -   Closing tags, such as `</p>` and `</div>`
    -   Plain text between tags that does *not* contain '<' or '>' characters

2.  Modify the tokenizer to handle `key="value"` attributes in opening tags.

3.  Write tests for your tokenizer.

You may use Python's own [re][py_re] module for tokenization.

### Efficiency {: .exercise}

The parser developed in this chapter creates and discards a lot of objects.
How can you make it more efficient?

### Nested lists {: .exercise}

Write a function that accepts a string representing nested lists containing numbers
and returns the actual list.
For example, the input `[1, [2, [3, 4], 5]]`
should produce the corresponding Python list.

### The Shunting Yard Algorithm {: .exercise}

1.  Use the [shunting-yard algorithm][shunting_yard_algorithm]
    to implement a tokenizer for a simple subset of arithmetic that includes:

    -   single-letter variable names
    -   single-digit numbers
    -   the `+`, `*`, and `^` operators, where `+` has the lowest precedence and `^` has the highest

2.  Write tests for your tokenizer.

### Using the right tools {: .exercise}

1.  Rewrite the regular expression parser from this chapter
    using the [pyparsing][pyparsing] module.

2.  Did learning this module take more or less time
    than solving the problem without it?
    How many times would you have to use the module to amortize its learning overhead?

