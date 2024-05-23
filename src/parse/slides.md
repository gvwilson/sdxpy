---
template: slides
title: "Parsing Text"
---

## The Problem

-   `"2023-*{pdf,txt}"` is easier to read and write
    than `Lit("2023-", Any(Either("pdf", "txt")))`

-   How can we translate the former into the latter?

1.  Group characters into [%g token "tokens" %]

2.  Use tokens to create an [%g abstract_syntax_tree "abstract syntax tree" %]

[% figure
   slug="parse-pipeline"
   img="pipeline.svg"
   alt="Parsing pipeline"
   caption="Stages in parsing pipeline."
%]

---

## Cases

-   Characters like `{` and `*` can be processed immediately

-   But "regular" characters need to be accumulated

    -   `Lit("abc")` rather than `Lit("a", Lit("b", Lit("c")))`

    -   When we encounter a special character or '}',
        we close the current literal token

-   The `,` character closes a literal but doesn't produce a token

---

## A Bit More Design

-   The result is the final (flat) list of tokens

-   We could pass around a list and append to it

-   But we also need to know the characters in each `Literal`
    and the options in each `Either`

-   So create a class rather than a function

    -   Easier than carrying state around explicitly

---

## Tokenizer

[%inc tokenizer.py mark=tok %]

---

## Tokenizer

-   Call `self._setup()` at the start so that the tokenizer can be re-used

-   *Don't* call `self._add()` for regular characters

    -   Add literals when we see special characters

    -   And after all the input has been parsed

---

## Adding Tokens

[%inc tokenizer.py mark=add %]

-   `self._add(None)` means "add the literal but nothing else"

[% figure
   slug="parse-tokenize"
   img="tokenize.svg"
   alt="Tokenizing"
   caption="Steps in tokenizing a string."
%]

---

## Testing

[%inc test_tokenizer.py mark=tests %]

-   Each sub-list represents one token

---

## Parsing

[%inc parser.py mark=parse %]

-   `front[0]` is the token's name, `front[1:]` is any other data

-   `back` is the remaining tokens

-   Look for a <code>\_parse\_<em>thing</em></code> method to handle each token

---

<!--# class="aside" -->

## Introspection and Dispatch

-   [%g introspection "Introspection" %]:
    having a program look up a function or method inside itself
    while it is running

-   [%g dynamic_dispatch "Dynamic dispatch" %]:
    using introspection to decide what to do next
    rather than a long chain of `if` statements

-   These are powerful techniques and we use them frequently

---

## Fill in the Simple Stuff

[%inc parser.py mark=simple %]

-   Hardest part is making sure to name them properly
    so that `_parse` can find them

---

## `Either` is Messy

[%inc parser.py mark=either %]

-   Remember, we didn't save the commas
-   It really should pull things from `back` until it hits `EitherEnd`

---

## A Better Implementation

[%inc better_parser.py mark=either %]

---

## Testing

[%inc test_parser.py mark=sample %]

-   But this assumes we can compare `Match` objects

---

<!--# class="aside" -->

## They're Just Methods

-   `a == b` is "just" `a.__eq__(b)`
-   [%g operator_overloading "Operator overloading" %]:
    if our class has methods with the right names,
    Python calls them to perform "built-in" operations
-   Parent `Match` class does shared work
    -   E.g., make sure objects have
        the same [%g concrete_class "concrete class" %]
-   Child method (if any) does details
    -   E.g., make sure two `Lit` objects are checking for the same text

---

## Infrastructure

[%inc match.py mark=equal %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="parse-concept-map"
   img="concept_map.svg"
   alt="Concept map of parsing"
   caption="Concept map"
%]
