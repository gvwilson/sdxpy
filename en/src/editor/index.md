---
title: "An Editor"
syllabus:
-   A terminal UI (TUI) can do most of the things that graphical UIs can do.
-   TUI libraries provide a screen abstraction to encapsulate the details of different platforms' terminal applications.
-   Most terminal applications are built around an event loop that waits for user input and takes appropriate action.
-   When testing user interfaces, we usually assume that the rendering layer is working correctly.
-   A text editor must translate between the coordinate systems of the text and the screen.
-   Using a lookup table to map events to actions simplifies design and testing.
---

Early text editors were line-at-a-time applications like the debugger of [%x debugger %].
Most people prefer to use full-screen interactive editors,
so this chapters builds a simple one to show how they work.
Our design follows [%i "Lorgat, Wasim" %][Wasim Lorgat][lorgat_wasim][%/i%]'s
[tutorial][lorgat_editor] closely,
and borrows a few ideas from [%i "Equivias, Cristian" %][Cristian Esquivias[%/i%]'s
[`ted` editor][ted_editor] as well.

Our starting point is Python's [curses][py_curses] module.
It gives programs access to a library called `curses`,
which provides a uniform interface to terminal applications on several platforms.
These applications can do much more than most people realize—libraries like [Textualize][textualize]
can create [%i "terminal UI (TUI)" %][%g tui "terminal UIs" %][%/i%] (TUIs)
that can do most of what a modern browser can do,
but we will keep things simple for now.

## Logging Keystrokes {: #editor-keystrokes}

Let's started by writing a terminal application
that does nothing except wait for a command to quit:

[% inc file="simplest.py" %]

Our application is in a function called `main`.
Instead of calling it directly,
we pass it to `curses.wrapper`,
which initializes the terminal library for us
and then calls our function with an object
that represents the terminal.
`main` then goes into an [%i "event loop" %][%g event_loop "event loop" %][%/i%]
that waits for a keystroke
and quits if the key is either 'Q' or 'q'.

When we run this program our terminal window goes blank
and stays that way until we quit.
To convince ourselves that it's actually doing something,
we can modify it to save keystrokes to a file for later inspection:

[% inc file="log_keystrokes.py" %]

We can then test the program interactively
or send characters to standard input
(making sure to send 'Q' as the last character
so that the application exits):

[% inc pat="log_keystrokes.*" fill="sh out" %]

<div class="callout" markdown="1">

### Taking it on Faith

Testing interactive applications like this one is harder than testing code libraries.
The problem isn't with input:
as the example above shows,
we can send characters to standard input pretty easily.
The problem is that we have no easy way to check what the application displays in response.
We can check whether it (for example) told the terminal to display the letter 'A'
or (in a more complex application) told the browser window to scroll,
but how can we be sure that it actually did those things?
At some point we must either watch the tests drive the application
(which many programmers do as a last check)
or just trust that the layer below ours is doing the right thing.

</div>

## Displaying a File {: #editor-file}

As mentioned in [%x layout %],
a screen's [%i "coordinate system" %]coordinate system[%/i%] is upside down:
for historical reasons,
the Y axis starts at the top and increases going down.
Once we've come to terms with that quirk,
though,
displaying a file is straightfoward:
we call the screen object's `addstr` method
with a location and some text:

[% inc file="show_file.py" keep="main" %]

Once `main` has displayed
the [%i "buffer (text)" %][%g buffer "text buffer" %][%/i%] it has been given,
it waits for a command to quit.
The text can come from anywhere—here,
we read it from a file and pass it as an extra argument to `curses.wrapper`,
which in turn passes it to `main`:

[% inc file="show_file.py" keep="launch" %]

<div class="callout" markdown="1">

### Why is it Called a Buffer?

The word "buffer" originally meant something that lessened or absorbed an impact.
In computing,
the word is used for a temporary storage area for data.
The former became the latter because
input and output devices often work in bursts
that can temporarily outrun a computer's processing power.
It's therefore common practice to set aside some memory to hold
input that hasn't been processed yet
or output that hasn't yet been displayed.
The term then became used more generally.

</div>

Our little program can now display text,
but only in small amounts.
If we try to display a thousand lines,
each of which is a thousand characters long,
we get an error:

[% inc file="fail_large.py" keep="launch" %]
[% inc file="fail_large.out" %]

The problem is that we're trying to write outside the physical window.
The solution is to trim what we're displaying to fit inside the available area.
Let's define a `Window` class to keep track of the display area:

[% inc file="show_large.py" keep="window" %]

When the main program starts,
it askes the curses module how many lines and columns are available,
uses those values to initialize a `Window`,
and then only shows the text that lies inside the window:

[% inc file="show_large.py" keep="main" %]

We don't really need a `Window` class
if all we want to do is trim some lines of text to fit a window.
However,
a real text editor needs to deal with the user resizing the window
(which we will tackle in the exercises),
scrolling (which we tackle below),
and similar events.
By combining the X and Y dimensions of the rendering area in a class now,
we will save ourselves a lot of rewriting later.

## An Editor Object {: #editor-object}

If we are representing the window as a class,
it's natural to use one for the editor as well.
However,
`curses.wrapper` requires a function as a starting point.
We can satisfy that need by creating a class with a `__call__` method
so that instances of the class can be "called" as if they were functions.
When we do this,
though,
we must use the [%i "Delayed Construction pattern" %][%g delayed_construction_pattern "Delayed Construction" %][%/i%] design pattern,
because we won't have all the information we need to build the editor object
at the moment that we need to create it.

Let's start by creating the editor class:

[% inc file="editor_class.py" keep="editor" %]

The constructor creates variables to hold the screen (which the curses module gives us)
and the window (which will be an instance of our `Window` class),
but initializes them both to `None`.
{: .continue}

When the object is "called"
(i.e., when its `__call__` method is invoked),
it fills in these variables and then starts to interact with the user.
The setup code is:

[% inc file="editor_class.py" keep="setup" %]

and the interaction is:
{: .continue}

[% inc file="editor_class.py" keep="interact" %]

We could test this by reading in a file,
but let's create 1000×1000 characters instead:

[% inc file="editor_class.py" keep="launch" %]

While we're creating a class,
let's build in a lookup table like the one in [%x interpreter %]
that translates characters to actions:

[% inc file="editor_interact.py" keep="init" %]

Each action must be a method with no arguments other than `self`
so that they can be called interchangeably:
{: .continue}

[% inc file="editor_interact.py" keep="quit" %]

Finally, we modify the `interact` method to look up actions and execute them:
{: .continue}

[% inc file="editor_interact.py" keep="quit" %]

## Moving Around {: #editor-move}

Our editor isn't much of an editor right now:
we can't even move around the text,
much less change it.
As first step toward fixing that,
let's define a `Cursor` class to keep track of the cursor's current location:

[% inc file="editor_move.py" keep="cursor" %]

The editor's constructor creates a variable to hold a cursor
(but doesn't fill it in yet—that will happen in the `setup` method).
It also adds entries to the action table for the four arrow keys:

[% inc file="editor_move.py" keep="init" %]

Each time we redraw the screen,
we display the cursor at its current location:

[% inc file="editor_move.py" keep="display" %]

Finally,
the methods that move the cursor change its X and Y coordinates:
{: .continue}

[% inc file="editor_move.py" keep="move" %]

This works—until we are at the end of a long line
and try to move up or down to a shorter one.
When we do that,
our X coordinate is past the end of the line we're on.
The solution is to trim the X coordinate each time we move up or down:

[% inc file="editor_move_fixed.py" keep="move" %]

but the need for this certainly isn't obvious.
As with most software,
we learn what the program needs from the program as we're writing it.
{: .continue}

All right:
we can move around the text,
but only around the portion we initially display
(which is the upper left of the whole thing).
We want users to be able to see all the available content,
which means we need to map locations in the text
to locations on the screen.
Let's enhance the `Window` class to keep track of the top row it's displaying
so that we can scroll vertically
(we'll leave horizontal scrolling as an exercise):

[% inc file="editor_scroll.py" keep="window" %]

When we display, we show the rows that are currently visible:

[% inc file="editor_scroll.py" keep="display" %]

The `translate` method turns the cursor's position into a content position:

[% inc file="editor_scroll.py" keep="translate" %]

Finally, we adjust the screen when moving:

[% inc file="editor_scroll.py" keep="updown" %]

Keeping track of the coordinate systems and their relation to each other is hard,
in part because we use the same words for both.
("Wait, do you mean the X coordinate in the text,
the X coordinate on the screen,
or the X coordinate of the cursor?")
Diagrams make all of this a lot easier to understand,
since programmers insist on using data formats that are backward compatible with punch cards,
we can't insert diagrams in source files
the way we can insert them into office documents.
Until we can,
there are always tools like [ASCIIFlow][asciiflow].

## Editing {: #editor-editing}

We are finally ready to actually edit something.
Since we're going to be changing the text,
we create a `Buffer` class to store it.
This class checks that it's being constructed with a list of strings rather than a single string
(because that was a mistake we made several times when writing the code).
It also uses `__len__` and `__getitem__` so that it looks like a list,
which means no existing code needs to change:

[% inc file="editor_buffer.py" keep="buffer" %]

The only significant change to `Editor` is to ask the buffer what its bottom line is:

[% inc file="editor_buffer.py" keep="down" %]

That method in the `Buffer` class is just one line long:
{: .continue}

[% inc file="editor_buffer.py" keep="bottom" %]

Everything we have built so far just works after these changes,
which is a sign of good design.
{: .continue}

Now we can define the set of characters that users are allowed to insert.
For now,
we will stick to visible characters plus space;
we will handle newlines, tabs, and so on in the exercises.
We don't define these character classes ourselves:
instead, we rely on Python's [string][py_string] module.

[% inc file="editor_insert.py" keep="string" %]

We could add an action method for each character,
but for now it's simpler to modify `interact` to handle two cases separately:

[% inc file="editor_insert.py" keep="interact" %]

Finally,
we can go back to the `Buffer` class and insert the character:

[% inc file="editor_insert.py" keep="insert" %]

We are now able to edit a file.

## Exercises {: #editor-exercises}

### Why subtract one? {: .exercise}

Our programs get the number of lines and columns from the curses module
but then subtract 1 from each
to initialize the `Window` object.
Why do we need to do this?
What happens if we use the number of lines and columns directly?

### Resizing the window {: .exercise}

The curses module tells a program that the user has resized the window
by giving the program a `KEY_RESIZE` key.
Modify the editor to handle this.

### Horizontal scrolling {: .exercise}

Modify the editor to support horizontal scrolling as well as vertical scrolling.

### Deleting characters {: .exercise}

Modify the editor so that users can delete characters.
What happens if someone tries to delete a character when the cursor is at the start of the line?

### Saving changes {: .exercise}

Modify the editor so that if it was launched by reading a file,
typing Ctrl-W will write (save) that same file.

### Splitting lines {: .exercise}

Modify the editor so that if the user types Enter in the middle of a line,
the line splits.

### Paging {: .exercise}

Use the curses module to create a tool for paging up and down through files
like the Unix `less` command.

### Marking locations {: .exercise}

Modify the editor so that Ctrl-X records the current location of the cursor
and Ctrl-J jumps the cursor back to that location.

### Status line {: .exercise}

Add a status line to the bottom of the editor
that shows the name of the file currently being edited
and the XY coordinates of the cursor within the text buffer.

### Justify paragraphs {: .exercise}

Modify the editor so that when the user types Ctrl-U
it justifies the text in the current paragraph.
