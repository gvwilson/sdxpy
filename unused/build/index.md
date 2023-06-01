## Variables {: #builder-variables}

We don't want to have to write a hundred nearly-identical recipes
if our program has a hundred files
or our website has a hundred blog posts.
Instead,
we want to write generic [%i "build!rule" "rule (in build)" %]build rules[%/i%].
To do this we need:

-   a way to define a set of files;

-   a way to specify a generic rule;
    and

-   a way to fill in parts of that rule.

We will achieve this by overriding `build_graph` to replace variables in recipes with values.
Once again,
object-oriented programming lets us change only what we need to,
provided we divided our problem into sensible chunks in the first place.

<div class="callout" markdown="1">
### Extensibility and Experience

[%x interpreter %] said that one way to evaluate a program's design
is to ask how [%g extensibility "extensible" %] it is.
In practice,
extensibility usually comes from experience:
we can't know what [%g affordance "affordances" %] to provide
until we've tried extending our code in different ways a couple of times.
We [%g refactor "refactored" %] the examples in this book several times
as we wrote the explanations
so that early versions left room for later ones.
Don't be surprised or disappointed if you have to do this for your own code;
after you've extended and refactored something two or three times,
it usually settles down into its final form.
</div>

Make provides
[%i "automatic variable (in build)" "build!automatic variable" %][%g automatic_variable "automatic variables" %][%/i%]
with cryptic names like `$<` and `$@`
to represent the parts of a rule.
Our variables will be more readable:
we will use `@TARGET` for the target,
`@DEPENDENCIES` for the dependencies (in order),
and `@DEP[1]`, `@DEP[2]`, and so on for specific dependencies
([% f builder-pattern-rules %]).

[% figure
   slug="builder-pattern-rules"
   img="builder_pattern_rules.svg"
   alt="Pattern rules"
   caption="Turning patterns rules into runnable commands."
%]

Our variable expander looks like this:

[% inc file="expand_variables.py" keep="expand" %]

After adding this,
we immediately test that it works when there *aren't* any variables to expand
by running it on the same example we used previously:

[% inc pat="expand_variables_no_vars.*" fill="sh out" %]

This is perhaps the most important reason to create tests:
they tell us if something we have added or changed
has caused a [%g regression "regression" %],
i.e., has broken something that used to work.
If so,
the problem will be easier to fix while
the breaking change is still fresh in our minds.
{: .continue}

## Generic Rules {: #builder-generic}

Now we need to add [%i "pattern rule (in build)" "build!pattern rule" %][%g pattern_rule "pattern rules" %][%/i%]:
Our test rules file is:

[% inc file="pattern_rules.yml" %]

and our first attempt at reading it extracts rules before expanding variables:
{: .continue}

[% inc file="pattern_attempt.py" keep="body" %]

However,
it doesn't work:

[% inc pat="pattern_attempt.*" fill="sh out" %]

After a bit of poking around with a [%i debugger %]debugger[%/i%]
we realize that
the failure occurs when we're looking at the rule for `%.in`.
When we create edges in the graph between a target and its dependencies,
`networkx` automatically adds a node for the dependency
if one didn't exist yet.
As a result,
when we say that `%.out` depends on `%.in`,
we wind up with a node for `%.in` that doesn't have any recipes.

We can fix our problem by changing the `build_graph` method
so that it saves pattern rules in a dictionary
and then builds the graph from the non-pattern rules:

[% inc file="pattern_final.py" keep="build" %]

Expanding rules relies on two helper methods:
{: .continue}

[% inc file="pattern_final.py" keep="expand" %]

The first helper finds rules:
{: .continue}

[% inc file="pattern_final.py" keep="find" %]

and the second adds links and recipes to the graph:
{: .continue}

[% inc file="pattern_final.py" keep="fill" %]

We're finally ready to test:

[% inc pat="pattern_final.*" fill="sh out" %]
