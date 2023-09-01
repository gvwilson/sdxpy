---
syllabus:
-   The curses module manages text terminals in a platform-independent way.
-   Write debugging information to a log file when the screen is not available.
-   We can use a callable object in place of a function to satisfy an API's requirements.
-   Test programs using synthetic data.
-   Using delayed construction and/or factory methods can make code easier to evolve.
-   Refactor code before attempting to add new features.
-   Separate the logic for managing data from the logic for displaying it.
depends:
status: "revised 2023-08-14"
---

Before they need version control tools or interpreters,
programmers need a way to edit text files.
Even simple editors like Notepad and [Nano][nano] do a lot of things:
moving a cursor,
inserting and deleting characters,
and more.
This is too much to fit into one lesson,
so this chapter builds a tool for viewing files,
which [%x undo %] extends to create an editor with undo and redo.
Our example is inspired by [this tutorial][lorgat_tutorial]
written by [Wasim Lorgat][lorgat_wasim].

## Curses {: #viewer-curses}

Our starting point is the [`curses`][py_curses] module,
which handles interaction with text terminals on several different operating systems
in a uniform way.
A very simple curses-based program looks like this:

[% inc file="first_curses.py" %]

`curses.wrapper` takes a function with a single parameter as input,
does some setup,
and then calls that function with an object
that acts as an interface to the screen.
(It is called `stdscr`, for "standard screen",
by analogy with standard input `stdin` and standard output `stdout`.)
Our function `main` is just an infinite loop that consumes keystrokes
but does nothing with them.
When we run the program,
it clears the screen and waits for the user to interrupt it by typing Ctrl-C.

We'd like to see what the user is typing,
but since the program has taken over the screen,
`print` statements won't be of use.
Running this program inside a single-stepping debugger is challenging
for the same reason,
so for the moment we will cheat and create a [%g log_file "log file" %]
for the program to write to:

[% inc file="util.py" keep="log" %]

With this in hand,
we can rewrite our program to take the name of the log file
as its sole command-line argument
and print messages to that file to show the keys that are being pressed.
We can also modify the program so that when the user presses `q`,
the program exits cleanly:

[% inc file="logging_curses.py" keep="show" %]

Notice that we print the representation of the characters using `repr`
so that (for example)
a newline character shows up in the file as `'\n'`
rather than as a blank line.
{: .continue}

We are now ready to actually show some text.
Given a list of strings,
the revised `main` function below will repeatedly:

1.  clear the screen;

2.  display each line of text in the correct location;

3.  wait for a keystroke; and

4.  exit if the key is a `q`.

[% inc file="show_lines.py" keep="main" %]

Two things about this function need to be kept in mind.
First, as explained in [%x layout %],
screens put (0, 0) in the upper left rather than the lower left,
and increasing values of Y move down rather than up.
To make things even more confusing,
`curses` uses (row, column) coordinates,
so we have to remember to write (y, x) instead of (x, y).

The other oddity in this function is that
it erases the entire screen each time the user presses a key.
Doing this is unnecessary in most cases—if
the user's action doesn't modify the text being shown,
there's no need to redraw it—but
keeping track of which actions do and don't require re-draw
would require extra code (and extra debugging).
For now,
we'll do the simple, inefficient thing.

Here's how we run our revised `main` function:

[% inc file="show_lines.py" keep="run" %]

From top to bottom,
we make a list of strings to display,
open the log file,
and then use `lambda` to make
an [%i "anonymous function" %]
that takes a single screen object as input (which `curses.wrapper` requires)
and immediately calls `main` with the two arguments that *it* requires.

A real text viewer would display the contents of a file,
but for development we will just make up a regular pattern of text:

[% inc file="util.py" keep="lines" %]

If we ask for five lines,
the pattern is:
{: .continue}

[% inc file="make_lines.out" %]

These lines are a very (very) simple example of [%g synthetic_data "synthetic data" %],
i.e.,
data that is made up for testing purposes.
If the viewer doesn't work for this text it probably won't work on actual files,
and the patterns in the synthetic data will help us spot mistakes in the display.
{: .continue}

## Windowing {: #viewer-window}

Our file viewer works,
but only for small examples.
If we ask it to display 100 lines,
or anything else that is larger than our screen,
it falls over with the message
`_curses.error: addwstr() returned ERR`
because it is trying to draw outside screen.
The solution is to create a `Window` class
that knows how big the screen is
and only displays lines (or parts of lines) that fit inside it:

[% inc file="use_window.py" keep="window" %]

Our `main` function is then:

[% inc file="use_window.py" keep="main" %]

Notice that `main` creates the window object.
We can't create it earlier and pass it into `main` as we do with `lines`
because the [%i "constructor" %] for `Window` needs the screen object,
which doesn't exist until `curses.wrapper` calls `main`.
This is an example of [%g delayed_construction "delayed construction" %],
and is going to constrain the rest of our design
([%f viewer-delayed %]).

[% figure
   slug="viewer-delayed"
   img="delayed.svg"
   alt="Delayed construction"
   caption="Order of operations in delayed construction"
%]

Nothing says we have to make our window exactly the same size as
the terminal that is displaying it.
In fact,
testing will be a lot simpler
if we can create windows of arbitrary size
(so long as they aren't *larger* than the terminal).
This version of `Window` takes an extra parameter `size`
which is either `None` (meaning "use the full terminal")
or a (rows, columns) pair specifying the size we want:

[% inc file="size_window.py" keep="window" %]

We're going to have a lot of two-dimensional (row, column) coordinates
in this program,
so let's define a pair constants `ROW` and `COL`
to be more readable than 0 and 1 or `R` and `C`.
(We should really create an [%g enumeration "enumeration" %],
but a pair of constants is good enough for now.)

[% inc file="util.py" keep="coord" %]
[% inc file="cursor_const.py" keep="window" omit="omit" %]

## Moving {: #viewer-move}

Our program no longer crashes when given large input to display,
but we can't see any of the text outside the window.
To fix that,
we need to teach the application to scroll.
let's create another class to keep track of
the position of a cursor:

[% inc file="move_cursor.py" keep="cursor" %]

The cursor keeps track of its current (row, column) position in a list,
but `Cursor.pos` returns the location as a separate tuple
so that other code can't modify it.
In general,
nothing outside an object should be able to change
the data structures that object uses to keep track of its state;
otherwise,
it's very easy for the internal state to become inconsistent
in difficult-to-debug ways.
{: .continue}

Now that we have a way to keep track of where the cursor is,
we can tell `curses` to draw the cursor in the right location
each time it renders the screen:

[% inc file="move_cursor.py" keep="main" %]

As this code shows,
the screen's `getkey` method returns the names of the arrow keys.
And since `stdscr.move` takes two arguments
but `cursor.pos` returns a two-element tuple,
we [%i "spread" %] the latter with `*` to satisfy the former.

When we run this program and start pressing the arrow keys,
the cursor does indeed move.
In fact,
we can move it to the right of the text,
or below the bottom line of the text
if there are fewer lines of text than rows in our window.
What's worse,
if we move the cursor off the left or top edges of the screen
our program crashes with the message
`_curses.error: wmove() returned ERR`.
And we still can't see all the lines in a long "file":
the text doesn't scroll down when we go to the bottom.

We need to constrain the cursor's movement
so that it stays inside the text (not just the window),
while simultaneously moving the text up or down when appropriate.
Before tackling those problems,
we will reorganize the code
to give ourselves a better starting point.

## Refactoring {: #viewer-refactor}

Our first change is to write a class to represent
the application as a whole;
our program will then create one instance of this class,
which will own the window and cursor.
The trick to making this work is to take advantage of
one of the [%i "protocol" "protocols" %] introduced in [%x protocols %]:
if an object has a method named `__call__`,
that method will be invoked when the object is "called" as if it were a function:

[% inc pat="call_example.*" fill="py out" %]

Since the `MainApp` class below defines `__call__`,
`curses.wrapper` believes we have given it the single-parameter function it needs:

[% inc file="main_app.py" keep="main" %]

The `__call__` method calls `_setup`
to create and store the objects the application needs,
then `_run` to handle interaction.
The latter is:

[% inc file="main_app.py" keep="run" %]

Finally,
we pull the startup code into a function `start`
so that we can use it in future versions of this code:

[% inc file="util.py" keep="start" %]

and then launch our application like this:
{: .continue}

[% inc file="main_app.py" keep="launch" %]

Next,
we refactor `_run` to handle keystrokes using [%i "dynamic dispatch" %]
instead of a long chain of `if`/`elif` statement:

[% inc file="dispatch_keys.py" keep="interact" %]

A little experimentation showed that
while the `curses` module uses names like `"KEY_DOWN"` for arrow keys,
it returns actual [%i "control code" "control codes" %]
for key combinations like Ctrl-X.
The `TRANSLATE` dictionary turns these into human-readable names
that we can glue together with `_do_` to make a method name;
we got the hexadecimal value `"\x18"` by logging keystrokes to a file
and the looking at its contents.
We could probably have found this value in some documentation somewhere
if we had looked hard enough,
but a ten-second experiment seemed simpler.

With `_interact` in place,
we can re-write `_run` to be just five lines long:

[% inc file="dispatch_keys.py" keep="main" %]

It now relies on a member variable called `_running`
to keep the loop going.
We could have had each key handler method return `True` or `False`
to signal whether to keep going or not,
but we found out that the hard way that
it's very easy to forget to do this,
since almost every handler method's result is going to be the same.

<div class="callout" markdown="1">

### Inheritance

`DispatchApp` [%i "inheritance" "inherits" %] from our first `MainApp`
so that we can recycle the initialization code we wrote for the latter.
To make this happen,
`DispatchApp.__init__` [%i upcall "upcalls" %] to `MainApp.__init__`
using `super().__init__`.
We probably wouldn't create multiple classes in a real program,
but doing this simplifies exposition when teaching.
In order to make this work cleanly,
we did have to move some code around
as later examples showed us that
we should have divided things up differently in earlier examples.

*This is normal.*
Nobody has perfect foresight;
if we haven't built a particular kind of application several times,
we can't anticipate all of the [%i "affordance" "affordances" %] we might need,
so going back and refactoring old code to make new code easier to write
is perfectly natural.
If we need to refactor every time we want to add something new,
though,
we should probably rethink our design entirely.

</div>

We now have classes to represent the application, the window, and the cursor,
but we are still storing the text to display as a naked list of lines.
Let's wrap it up in a class:

[% inc file="buffer_class.py" keep="buffer" %]

This [%g buffer_text "text buffer" %] class doesn't do much yet,
but will later keep track of the viewable region.
Again,
we make a copy of `lines` rather than using the list the caller gives us
so that other code can't change the buffer's internals.
The corresponding change to the application class is:

[% inc file="buffer_class.py" keep="app" %]

<div class="callout" markdown="1">

### Factory Methods

We want to re-use as much of `BufferApp` as possible
in upcoming versions of our file viewer.
If `setup` calls the constructors of specific classes
to create the window, buffer, and cursor objects,
we will have to rewrite the entire method
each time we change which classes we want to use
for any of those three things.
Putting constructor calls in [%g factory_method "factory methods" %]
makes the code longer,
but allows us to override them one by one.
We didn't do this when we were first writing these examples;
instead,
as described in the previous callout,
we went back and refactored earlier classes
to make later ones easier.

</div>

## Clipping {: #viewer-clip}

We are now ready to keep the cursor inside
both the text and the screen.
The `ClipCursor` class below takes the buffer as a constructor argument
so that it can ask how many rows there are
and how big each one is,
but its `up`, `down`, `left`, and `right` methods
have exactly the same [%i "signature" "signatures" %] as
the corresponding methods in the original `Cursor` class.
As a result,
while we have to change the code that *creates* a cursor,
we won't have to make any changes to the code that *uses* the cursor:

[% inc file="clip_cursor.py" keep="cursor" %]

The logic in the movement methods in `ClipCursor` is relatively straightforward.
If the user wants to go up,
don't let the cursor go above line 0.
If the user wants to go down,
on the other hand,
don't let the cursor go below the last line,
and so on.
These methods rely on the buffer being able to report
the number of rows it has
and the number of columns in a particular row,
so we define a new `ClipBuffer` class that provides those,
and then override the `_make_buffer` and `_make_cursor` methods
in the application class
to construct the appropriate objects
*without* changing the kind of window we are creating:

[% inc file="clip_cursor.py" keep="other" %]

When we run this program,
we are no longer able to move the cursor outside the window
or outside the displayed text—unless,
that is,
we go to the end of a long line and then move up to a shorter one.
The problem is that `up` and `down` only change
the cursor's idea of the row it is on,
and don't check that the column position is still inside the text.
The fix is simple:

[% inc file="clip_fixed.py" keep="cursor" %]

One sign of a good design is that
there is one (hopefully obvious) place to make a change
in order to fix a bug or add a feature.
By that measure,
we seem to be on the right track.
{: .continue}

## Viewport {: #viewer-continue}

We are finally ready to scroll the text vertically
so that all of the lines can be seen
no matter how small the window is.
(We will leave horizontal scrolling as an exercise.)
A full-featured editor would introduce another class,
often called a [%g viewport "viewport" %],
to track the currently-visible portion of the buffer.
To keep things simple,
we will add two member variables to the buffer instead
to keep track of the top-most visible line
and the height of the window:

[% inc file="viewport.py" keep="buffer" %]

The most important change in the buffer is that
`lines` returns the visible portion of the text
rather than all of it.
Another change is that the buffer initializes `_height` to `None`
and requires someone to set it to a real value later
because the application's `_setup` method
creates the cursor, buffer, and window independently.
If we were building a single class
rather than layering tutorial classes on top of each other,
we would probably go back and change `_setup`
to remove the need for this.
{: .continue}

Our buffer also gains two more methods.
The first transforms the cursor's position from buffer coordinates
to screen coordinates:

[% inc file="viewport.py" keep="transform" %]

The second moves `_top` up or down when we reach the edge of the display:

[% inc file="viewport.py" keep="scroll" %]

As before,
we derive a new application class to create the right kind of buffer object.
We also override `_run` to scroll the buffer
after each interaction with the user:

[% inc file="viewport.py" keep="app" %]

Notice that the `ViewportApp` class creates a `ViewportCursor`.
When we were testing the program,
we discovered that we had introduced a bug:
the cursor could go outside the window again
if the line it was currently on
was wider than the window.
The solution is to add another check to `_fix`
and to ensure that left and right movement constrain the cursor's position
in the same way as vertical movement:

[% inc file="viewport.py" keep="cursor" %]

[%f viewer-inheritance %] shows the classes we have created
at each stage of this tutorial.
As we have said several times above,
if we were developing a file viewer for real use
we would probably have added features to classes
rather than repeatedly deriving new ones.
However,
we would probably have gone through the same sequence,
i.e.,
the history of our code in version control
would probably show the classes as presented here.
Again,
*this is normal.*

[% figure
   slug="viewer-inheritance"
   img="inheritance.svg"
   alt="Inheritance in lesson"
   caption="Class definitions and inheritance in lesson"
%]

## Summary {: #viewer-summary}

[% figure
   slug="viewer-concept-map"
   img="concept_map.svg"
   alt="Concept map of file viewer"
   caption="Concept map"
   cls="here"
%]

## Exercises {: #viewer-exercises}

### Using `global` {: .exercise}

1.  Why does the `open_log` function need the line `global LOG`?
    What happens if it is removed?

2.  Why doesn't the `log` function need this statement?

### Horizontal Scrolling {: .exercise}

Modify the application to scroll horizontally as well as vertically.

### Explain the Bug {: .exercise}

Replace the `ViewportCursor` class in the final version of the code
with the earlier `ClipCursorFixed` class,
then explain the bug `ViewportCursor` was created to fix.

### Line Numbers {: .exercise}

Modify the file viewer to show line numbers on the left side of the text.
