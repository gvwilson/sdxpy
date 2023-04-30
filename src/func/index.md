## Functions {: #interpreter-functions}

One way to evaluate the design of a piece of software is
to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things [%b Wilson2022a %].
The answer for our interpreter is now, "Pretty easily,"
but for our little language is, "Not at all,"
because there's no way for users to create new operations of their own.
We need to give users a way to define and call functions.

Doing this takes less than 60 lines:

1.  A function definition looks like:

    ```python
    ["def", "same", ["num"], ["get", "num"]]
    ```

    It has a name, a (possibly empty) list of parameter names,
    and a single instruction as a body
    (which will usually be a `"seq"` instruction).

2.  Functions are stored in the environment like any other value.
    The value stored for the function defined above would be:

    ```python
    ["func", ["num"], ["get", "num"]]
    ```

    We don't need to store the name: that's recorded by the environment,
    just like it is for any other variable.

3.  A function call looks like:

    ```python
    ["call", "same", 3]
    ```

    The values passed to the functions are normally expressions rather than constants,
    and are *not* put in a sub-list.
    The implementation:
    1.  Evaluates all of these expressions.
    2.  Looks up the function.
    3.  Creates a new environment whose keys are the parameters' names
        and whose values are the expressions' values.
    4.  Calls `do` to run the function's action and captures the result.
    5.  Discards environment created two steps previously.
    6.  Returns the function's result.

4.  Instead of using a single dictionary to store an environment
    we use a list of dictionaries.
    The first dictionary is the global environment;
    the others store the variables belonging to active function calls.

5.  When we get or set a variable,
    we check the most recent environment first
    (i.e., the one that's last in the list);
    if the variable isn't there we look in the global environment.
    We don't look at the environments in between;
    the exercises explore why not.

<div class="callout" markdown="1">

### Scoping rules

The set of active environments makes up the program's
[%i "call stack" %][%g call_stack "call stack" %][%/i%].
For historical reasons,
each environment is sometimes called a [%i "call stack!stack frame" "stack frame" %][%g stack_frame "stack frame" %][%/i%].
Searching through all active stack frames for a variable
is called is [%i "dynamic scoping" "scoping!dynamic" %][%g dynamic_scoping "dynamic scoping" %][%/i%].
In contrast,
most programming languages used [%i "lexical scoping" "scoping!lexical" %][%g lexical_scoping "lexical scoping" %][%/i%],
which figures out what a variable name refers to based on the structure of the program text.

</div>

Here's the implementation of `do_def`:

[% inc file="func.py" keep="def" %]

And here's the implementation of `do_call`:
{: .continue}

[% inc file="func.py" keep="call" %]

Our test program and its output are:
{: .continue}

[% inc pat="func.*" fill="tll out" %]

Once again,
Python and other languages work exactly as shown here.
The interpreter
(or the CPU, if we're running code compiled to machine instructions)
reads an instruction,
figures out what operation it corresponds to,
and executes that operation.

