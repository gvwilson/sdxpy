---
syllabus:
-   Replace user interface components with mock objects to simplify testing.
-   Record actions and state to check behavior these mock objects.
-   Use objects to represent actions to record history and enable undo.
-   Recording state is easier but more expensive than recording changes.
depends:
-   persist
-   viewer
status: "revised 2023-08-14"
---

Viewing text files is useful,
but we'd like to be able to edit them as well.
This chapter therefore modifies the file viewer of [%x viewer %]
so that we can add and delete text.
And since people make mistakes,
we will also implement undo,
which will introduce another commonly-used design pattern.

## Getting Started {: #undo-start}

Our file viewer has four classes:

-   A `Window` can draw lines and report its size.

-   A `Buffer` stores lines of text,
    keeps track of a [%i "viewport" %],
    and transforms buffer coordinates to screen coordinates.

-   A `Cursor` knows its position in
    the [%i "buffer (of text)" "buffer" %]
    and can move up, down, left, and right.

-   The `App` makes a window, a buffer, and a cursor,
    then maps keys to actions.

To make unit testing simpler,
we start by adding one more class:
a replacement for the screen object provided by the [`curses`][py_curses] module.
This class stores the current state of the display in a rectangular grid
so that our tests can check it easily.
It also takes a list of keystrokes as input
to simulate interaction with the user:

[% inc file="headless.py" keep="screen" %]

GUI applications that don't display anything
are often called [%g headless "headless" %] applications.
Giving our simulated keystrokes to the screen seems odd—it would make more sense
for `App` to have a method that gets keystrokes—but
it's the simplest way to fit everything in beside
the classes we already have.
{: .continue}

<div class="callout" markdown="1">

### Clean Exit

Notice that when the screen runs out of simulated keystrokes
it produces `CONTROL_X`,
meaning "exit the application".
We need this to break out of the keystroke-processing loop in the application,
and no,
we didn't think of this up front…

</div>

To finish this change,
we also need to define a `HeadlessWindow`
that takes a desired screen size and passes it to the screen:

[% inc file="headless.py" keep="window" %]

Finally,
our new application class records keystrokes,
the cursor position,
and the screen contents for testing:

[% inc file="headless.py" keep="app" %]

We can now write tests like this:

[% inc file="test_headless.py" keep="example" %]

## Insertion and Deletion {: #undo-indel}

We are now ready to implement insertion and deletion.
The first step is to add methods to the buffer class
that update a line of text:

[% inc file="insert_delete.py" keep="buffer" %]

Notice that we delete the character *under* the cursor,
not the one to the left of the cursor:
this is delete-in-place rather than backspace-delete.
Notice also that we have done a little [%i "defensive programming" %]
by checking that the coordinates given for the operation make sense.
{: .continue}

The window, cursor, and screen don't need to change
to support insertion and deletion,
but the application class needs several updates.
The first is to define the set of characters that can be inserted,
which for our example will be letters and digits,
and to create a buffer of the appropriate kind:

[% inc file="insert_delete.py" keep="app" %]

We also need to create handlers for insertion and deletion:

[% inc file="insert_delete.py" keep="action" %]

Finally,
since we don't want to have to add one handler
for each insertable character,
let's write a `_get_key` method that returns a pair of values.
The first indicates the "family" of the key,
while the second is the actual key.
If the family is `None`,
the key is a special key with its own handler;
otherwise,
we look up the handler for the key's family:

[% inc file="insert_delete.py" keep="dispatch" %]

We're going to write a lot of tests for this application,
so let's write a [%i "helper function" %]
to create a [%i "fixture" %],
run the application,
and return it:

[% inc file="test_insert_delete.py" keep="fixture" %]

Our tests are now straightforward to set up and check:

[% inc file="test_insert_delete.py" keep="example" %]

<div class="callout" markdown="1">

### Edge Case

One of our tests uncovers the fact that
our application crashes if we try to delete a character
when the buffer is empty:

[% inc file="test_insert_delete.py" keep="empty" %]

Our focus is implementing undo,
so we will leave fixing this for an exercise.
{: .continue}

</div>

## Going Backward {: #undo-backward}

In order to undo things we have to:

1.  keep track of *actions* and reverse them, or

2.  keep track of *state* and restore it.

Recording actions can be trickier to implement
but requires less space than saving the entire state of the application
after each change,
so that's what most systems do.
The starting point is to append a record of every action to a log:

[% inc file="history.py" keep="app" %]

But what about undoing cursor movement?
If we add a character,
move to another location,
and then undo,
shouldn't the cursor go back to where it was before deleting the character?
And how are we going to interpret these log records?
Will we need a second dispatch method with its own handlers?

The common solution to these problems is to use
the [%g command_pattern "Command" %] [%i "design pattern" %].
This pattern turns verbs into nouns,
i.e.,
each action is represented as an object
with methods to go forward and backward.
Our actions all derive from an [%g abstract_base_class "abstract base class" %]
so that they can be used interchangeably.
That base class is:

[% inc file="action.py" keep="Action" %]

The [%i "child class" "child classes" %] for insertion and deletion are:

[% inc file="action.py" keep="Insert" %]

[% inc file="action.py" keep="Delete" %]

We could implement one class for each direction of cursor movement,
but instead choose to create a single class:

[% inc file="action.py" keep="Move" %]

This class records the new cursor position as well as the old one
to make debugging easier.
It depends on adding two new methods to `Cursor`
to move in a particular direction by name
(e.g., "right" or "left")
and to move to a particular location:

[% inc file="cursor.py" keep="extra" %]

Our application's `_interact` method changes too.
Instead of relying on keystroke handler methods to do things,
it expects them to create action objects
([%f undo-verbs %]).
These objects are appended to the application's history,
and then asked to do whatever they do:

[% inc file="action.py" keep="interact" %]

[% figure
   slug="undo-verbs"
   img="verbs.svg"
   alt="Nouns as verbs in the Command pattern"
   caption="Representing actions as objects in the Command design pattern"
   cls="here"
%]

Note that we have modified all the handler methods
to take the keystroke as an input argument
so that we don't have to distinguish between
cases where it's needed and cases where it isn't.
This simplifies the code a little
at the expense of introducing unused parameters into
the handlers for special keys like cursor movement.
{: .continue}

Finally,
each handler method now builds an object and returns it:

[% inc file="action.py" keep="actions" %]

With all these changes in place
our application *almost* works.
We add an `_do_UNDO` handler that pops the most recent action from the history
and calls its `undo` method.
When we test this,
though,
we wind up in an infinite loop because
we are appending the action to the history before doing the action,
so we are essentially undoing our undo forever.
The solution is to modify the base class `Action` to have a `.save` method
that tells the application whether or not to save this action.
The default implementation returns `True`,
but we override it in `Undo` to return `False`:

[% inc file="undoable.py" keep="Undo" %]

Note that popping the most recent action off the history stack
only works once we modify the application's `_interact` method
so that it only saves actions that ought to be saved:

{% inc file="undoable.py" keep="app" omit="skip" %]

We can now write tests like this to check that we can insert a character,
undo the action,
and get back the screen we originally had:

[% inc file="test_undoable.py" keep="example" %]

## Summary {: #undo-summary}

[% figure
   slug="undo-concept-map"
   img="concept_map.svg"
   alt="Concept map of undo"
   caption="Concept map"
   cls="here"
%]

## Exercises {: #undo-exercises}

### Combining Movement {: .exercise}

Modify the application so that successive movement operations are combined
into a single undo step.

### Forgetting Moves  {: .exercise}

Most editors do not save cursor movements in their undo history.
Modify the code in this chapter so that undo only works on
changes to the content being edited.

### Limiting History {: .exercise}

Modify the application so that only the most recent hundred operations can be undone.

### Breaking Lines {: .exercise}

Modify the code so that pressing the Enter key inserts a new line
or breaks the current line in two.
What information do you have to store to make this operation undoable?

### Re-doing Operations {: .exercise}

Implement a "redo" command that re-executes an operation that has been undone.
How does redo differ from undoing an undo?
Does it make sense to redo an action that wasn't done?

### Repeating Operations {: .exercise}

1.  Implement a command to repeat the most recent operation.

2.  How should repeated operations be represented in the application's history?

### Saving Operations {: .exercise}

Use the ideas of [%x persist %] to save operations to a file and reload them
so that users can resume editing sessions.
