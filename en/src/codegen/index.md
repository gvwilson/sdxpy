---
title: "A Code Generator"
syllabus:
- FIXME
---

## Modifying Code {: #codegen-modify}

- Original code

[% inc file="double_and_print.py" %]

- Modifying code

[% inc file="unparse.py" keep="modify" %]
[% inc file="unparse_modified.out" %]

- Run it to check

[% inc file="unparse.py" keep="exec" %]
[% inc file="unparse_exec.out" %]

## Injecting a Counter {: #codegen-inject}

- What does a simple call look like?

[% inc file="call.py" %]
[% inc file="inject.py" keep="parse" %]
[% inc file="inject_parse.out" %]

- Construct an AST fragment that mirrors this

[% inc file="inject.py" keep="make" %]
[% inc file="inject_make.out" %]

- Modify source code

[% inc file="inject.py" keep="modify" %]

- Some test code

[% inc file="add_double.py" %]
[% inc file="inject_modified.out" %]

- Create a counter

[% inc file="inject.py" keep="counter" %]

- Test it

[% inc file="inject.py" keep="exec" %]
[% inc file="inject_exec.out" %]

## Exercises {: #codegen-exercises}

FIXME
