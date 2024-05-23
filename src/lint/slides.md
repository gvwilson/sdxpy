---
template: slides
title: "A Code Linter"
---

## The Problem

-   Want to check that our code follows style rules

-   And doesn't do things that are likely to be bugs

-   Build a [%g linter "linters" %]

    -   Checks for "fluff" in code

---

## Programs as Trees

-   [%x check %] represented HTML as a [%g dom "DOM tree" %]

-   We can represent code as an [%g abstract_syntax_tree "abstract syntax tree" %] (AST)

-   Each node represents a syntactic element in the program

---

## Programs as Trees

[%inc simple.py %]

[% figure
   slug="lint-ast-simple"
   img="ast_simple.svg"
   alt="Simple AST"
   caption="The abstract syntax tree for a simple Python program."
%]

---

## Building Trees

[%inc dump_ast.py %]
[%inc dump_ast_simple.out head="10" %]

---

## Finding Things

-   Could walk the tree to find `FunctionDef` nodes and record their `name` properties

-   But each node has a different structure,
    so we would have to write a recursive function for each type of node

-   [`ast`][py_ast] module's `ast.NodeVisitor` implements
    the [%g visitor_pattern "Visitor" %] pattern

-   Each time it reaches a node of type `Thing`, it looks for a method `visit_Thing`

---

## Collecting Names

[%inc walk_ast.py mark=class %]

---

## Collecting Names

1.  `CollectNames` constructors invokes `NodeVisitor` constructor
    before doing anything else

1.  `visit_Assign` and `visit_FunctionDef` must call `self.generic_visit(node)` explicitly
    to recurse

1.  `position` methods uses the fact that every AST node remembers where it came from

---

## Collecting Names

[%inc walk_ast.py mark=main %]
[%inc walk_ast.sh %]
[%inc walk_ast.out %]

---

## What Does This Do?

[%inc has_duplicate_keys.py %]

1.  An error
2.  Keeps the first
3.  Keeps the last
4.  Concatenates

[%inc has_duplicate_keys.out %]

---

## Finding Duplicate Keys

[%inc find_duplicate_keys.py mark=class %]
[%inc find_duplicate_keys.out %]

---

## False Negatives

-   Our duplicate finder only detects constants

[%inc function_keys.py %]

-   Fundamental theoretical result in computer science is that
    it's impossible to build a general-purpose algorithm
    that predicts the output of a program

---

## Finding Unused Variables

-   Not wrong, but clutter makes code harder to read

-   Have to take [%g scope "scope" %] into account

-   So keep a stack of scopes

[%inc find_unused_variables.py mark=class %]

---

## Recording Scope

-   Use `namedtuple` from Python's standard library

[%inc find_unused_variables.py mark=scope %]

---

## Bucketing

-   If the variable's value is being read,
    `node.ctx` (short for "context") is an instance of `Load`

-   If the variable is being written to,
    `node.ctx` is an instance of `Store`

[%inc find_unused_variables.py mark=name %]

---

## And Finally…

[%inc find_unused_variables.py mark=search %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="lint-concept-map"
   img="concept_map.svg"
   alt="Concept map for code manipulation"
   caption="Concepts for code manipulation."
%]
