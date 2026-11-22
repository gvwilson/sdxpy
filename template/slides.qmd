---
title: "A Template Expander"
---

<section class="slide" markdown="1">

## The Problem

-   Most pages on a site share some content

-   Many pages want to be customized based on data

-   So many sites use a templating system

    -   Turn data and HTML page with embedded directives into final page

</section>
<section class="slide" markdown="1">

## Design Options

1.  Embed commands in an existing language like [EJS][ejs]

2.  Create a mini-language with its own commands like [Jekyll][jekyll]

3.  Put directives in specially-named attributes in the HTML

[% figure
   slug="template-options"
   img="design_options.svg"
   alt="Three options for page templates"
   caption="Three different ways to implement page templating."
%]

-   We will use the third option so that we don't have to write a parser

</section>
<section class="slide" markdown="1">

## What Does Done Look Like?

[%inc loop.ht %]

-   `z-loop`: repeat this

-   `z-num`: a constant number

-   `z-var`: fill in a variable

-   `z-if`: conditional

</section>
<section class="slide" markdown="1">

## What Does Done Look Like?

[%inc loop.out %]

-   HTML doesn't care about extra blank lines, so we won't either

</section>
<section class="slide" markdown="1">

## How Do We Call This?

-   Design the [%g api "API" %] of our library first

[%inc example_call.py %]

-   In real life, `data` would come from a configuration file or database

</section>
<section class="slide" markdown="1">

## Managing Variables

-   Could use a `ChainMap`, but we'll write our own

[%inc env.py mark=body %]

</section>
<section class="slide" markdown="1">

## Visiting Nodes

-   Use the [%g visitor_pattern "Visitor" %] design pattern

[%inc visitor.py %]

</section>
<section class="slide" markdown="1">

## Expanding a Template

[%inc expander.py mark=construct %]

-   The environment

-   Handlers for our special node types

-   The result (strings we'll concatenate at the end)

</section>
<section class="slide" markdown="1">

## Open…

[%inc expander.py mark=open %]

-   If this is text, "display" it

-   If this is a special node, run a function

-   Otherwise, show the opening tag

-   Return value is "do we proceed"?

</section>
<section class="slide" markdown="1">

## …and Close

[%inc expander.py mark=close %]

-   Handlers come in open/close pairs

    -   Because some might need to do cleanup

</section>
<section class="slide" markdown="1">

## Managing Handlers

[%inc expander.py mark=handlers %]

-   `hasHandler` looks for attributes with special names

-   `getHandler` gets the one we need

</section>
<section class="slide" markdown="1">

## But What's a Handler?

[%inc z_num.py %]

-   A module with `open` and `close` functions

-   None of our handlers need state, so we don't need objects

</section>
<section class="slide" markdown="1">

## Variables Are Similar

[%inc z_var.py %]

-   We should think about error handling…

</section>
<section class="slide" markdown="1">

## Testing

[%inc template.py %]

</section>
<section class="slide" markdown="1">

## Static Text

-   If this doesn't work, nothing else will

[%inc static_text.ht %]
[%inc static_text.out %]

</section>
<section class="slide" markdown="1">

## Constants

[%inc single_constant.ht %]
[%inc single_constant.out %]

</section>
<section class="slide" markdown="1">

## Variables

[%inc single_variable.ht %]
[%inc single_variable.out %]

-   Input is a JSON file containing `{"varName": "varValue"}`

</section>
<section class="slide" markdown="1">

## Conditionals

[%inc z_if.py %]

-   The handler determines whether to show this tag and go deeper

-   What if the variable's value changes between opening and closing?

</section>
<section class="slide" markdown="1">

## Testing

[%inc conditional.ht %]
[%inc conditional.out %]

-   With JSON `{"yes": True, "no": False}`

</section>
<section class="slide" markdown="1">

## Loops

1.  Create a new stack frame holding the current value of the loop variable

1.  Expand all of the node's children with that stack frame in place

1.  Pop the stack frame to get rid of the temporary variable

</section>
<section class="slide" markdown="1">

## Loops

[%inc z_loop.py %]

-   The most complicated handler yet

</section>
<section class="slide" markdown="1">

## Testing

[%inc loop.ht %]
[%inc loop.out %]

</section>
<section class="slide" markdown="1">

## Next Steps

-   The `z-if` issue might mean we need state after all

-   Tackle that before going any further

-   And figure out how to do unit testing

</section>
<section class="slide" markdown="1">

## Summary

[% figure
   slug="template-concept-map"
   img="concept_map.svg"
   alt="Concept map for page templates"
   caption="Concept map."
%]

</section>
