---
title: "Object Persistence"
syllabus:
- FIXME
---

Database tables aren't the only way to save data.
Another option is to store objects as objects,
i.e.,
to save a list of dictionaries of dictionaries as-is
rather than flattering it into rows and columns.
Python's [pickle][py_pickle] module does this in a Python-specific way,
saving objects in a custom binary format,
while the [json][py_json] module saves some kinds of objects as text
formatted as [%g "json" JSON %],
which program written in other languages can read.

The phrase "some kinds of objects" is the most important part of the preceding paragraph.
Since programs can define new classes,
a persistence framework has to make one of the following choices:

1.  Only handle built-in types,
    or even more strictly,
    only handle types that are common across many languages,
    so that data saved by Python can be read by JavaScript and vice versa.

1.  Provide an easy way for programs to convert from user-defined types
    to built-in types
    and then save those.
    This choice is less restrictive
    but may lead to some information being lost:
    for example,
    if a program has a `User` class
    and instances of that class are saved as dictionaries,
    then the program that reads data might wind up with dictionaries instead of users.

1.  Save class definitions as well as objects' values
    so that when a program reads saved data
    it can reconstruct the classes
    and then create fully-functional instances of them.
    This choice is the most powerful,
    but it is also the hardest to implement,
    particularly across languages.
    It is also the riskiest:
    if a program is reading and then running saved methods,
    it has to trust that those methods aren't doing anything malicious.

This chapter starts by implementing the first option (built-in types only),
then extends it to handle [%g alias "aliases" %]
(which the JSON standard does not),
and finally adds ways to convert user-defined types to storable data.
To keep testing simple
we will store everything in flat text files;
to keep parsing simple
we will store one value per line
rather than using brackets and curly braces.

## Built-in Types {: #persistence-builtin}

The first thing we need to do is decide on a data format.
We will store each [%g atomic_value "atomic value" %] on a line of its own
with the type's name first and the value second.
For example,
the integer `123` will be saved as:

```
int:123
```

The function `save` handles three of Python's built-in types to start with:

[% inc file="builtin.py" keep="save" omit="extras" %]

The function that loads data starts by reading a single line,
stripping off the newline at the end
(which is added automatically by the `print` in `save`),
and then splitting the line on the colon.
After checking that there are two fields,
it uses the type name in the first field
to decide how to handle the second:

[% inc file="builtin.py" keep="load" omit="extras" %]

Saving a list is almost as easy:
we save the number of items in the list,
and then save each item with a recursive called to `save`.
For example,
the list `[55, True, 2.71]` is saved as:

```
list:3
int:55
bool:True
float:2.71
```

The code to do this is:

[% inc file="builtin.py" keep="save_list" %]

To load data we just read the specified number of items back into a list:

[% inc file="builtin.py" keep="load_list" %]

Notice that these two functions don't need to know
what kinds of values are in the list.
Each recursive call to `save` or `load`
advances the input or output stream
by precisely as many lines as it needs to.

Our functions handle sets in exactly the same was as lists;
the only difference is using the keyword `set` instead of the keyword `list`
in the opening line.
To save a dictionary,
we save the number of entries
and then save each key and value in turn:

[% inc file="builtin.py" keep="save_dict" %]

The code to load a dictionary is analogous.
{: .continue}

We now need to write some unit tests.
We will use two tricks when doing this:

1.  The `StringIO` class from Python's [io][py_io] module
    allows us to read from strings and write to them
    using the functions we normally use to read and write files.
    Using this lets us run our tests
    without creating lots of little files as a side effect.

1.  The `dedent` function from Python's [textwrap][py_textwrap] module
    removes leading indentation from the body of a string.
    Using this allows us to indent a textual [%g fixture "fixture" %]
    the same way we indent our Python code,
    which makes the test easier to read.

[% inc file="test_builtin.py" keep="test_save_list_flat" %]

We still need to decide how to save strings.
We can't just print them out because they might contain newlines,
which would break our reader.
One option would be to save each string's representation,
using the two-character [%g escape_sequence "escape sequence" %] `\n` for newline.
Instead,
we choose to break each string on newlines
and then save the number of lines
followed by each line.
For example,
the two-line text `"hello\nthere"` will be saved as:

```
str:2
hello
there
```

The `elif` branch to do this in `save` is:

[% inc file="builtin.py" keep="save_str" %]

and the corresponding clause in `load` is:
{: .continue}

[% inc file="builtin.py" keep="load_str" %]

## Converting to Classes {: #persistance-oop}

The `save` and `load` functions we built in the previous section work,
but as we were trying to extend them
we discovered that we had to modify their internals
every time we wanted to do something new.
As we said in [%x matching %],
the [%i "Open-Closed Principle" "software design!Open-Closed Principle" %][%g open_closed_principle "Open-Closed Principle" %][%/i%]
states that it should be possible to extend functionality
without rewriting existing code.
To make the next steps easier,
we will rewrite our functions as classes.

We will also use [%g dynamic_dispatch "dynamic dispatch" %]
to handle each item
instead of a multiway `if` statement.
The core of our saving class is:

[% inc file="oop.py" keep="save" %]

(We have called it `SaveOop` instead of just `Save`
because we are going to create several variations on it.)
{: .continue}

`SaveOop.save` figures out which method to call to save a particular thing
by constructing a name based on the thing's type,
checking whether that method exists,
and then calling it.
To make this work,
the methods that handle specific items
must all have the same [%g signature "signature" %]
so that they can be called interchangeably.
For example,
the methods that write integers and strings are:

[% inc file="oop.py" keep="save_examples" %]

`LoadOop.load` combines dynamic dispatch with
the string handling of our original `load` function:

[% inc file="oop.py" keep="load" %]

The methods that load individual items are even simpler:

[% inc file="oop.py" keep="load_float" %]

## Aliasing {: #persistence-aliasing}

Consider these two lines of code:

```python
shared = ["shared"]
fixture = [shared, shared]
```

They create the data structure shown on the left in [%fixme persistence-shared %],
but if we save this structure and then reload it
using what we have built so far
we will wind up with the data structure show on the right.
{: .continue}

[% fixme
   slug="persistence-shared"
   img="shared-wrong.svg"
   alt="Saving Aliased Data Incorrectly"
   caption="FIXME"
%]

In order to reconstruct the original data correctly we need to:

1.  keep track of everything we have saved;

1.  save a marker instead of the object itself
    when we try to save it a second time;
    and

1.  reverse this process when loading data.

Luckily,
Python has a built-in function called `id`
that returns a unique ID for every object in the program.
Even if two lists or dictionaries contain the same data,
`id` will report different IDs
because they're stored in different locations in memory.
We can use this to:

1.  store the IDs of all the objects we've already saved
    in a set, and then

1.  write a special entry with the keyword `alias`
    and its unique ID
    when we see an object for the second time.

Here's the start of `SaveAlias`:

[% inc file="aliasing_wrong.py" keep="save" %]

Its constructor creates an empty set of IDs-seen-so-far.
If `SaveAlias.save` notices that the object it's about to save
has been saved before,
it writes a line like this:
{: .continue}

```
alias:12345678:
```

where `12345678` is the object's ID.
Otherwise,
it saves the object's type,
its ID,
and either its value or its length:

[% inc file="aliasing_wrong.py" keep="save_list" %]

`SaveAlias._list` is a little different from `SaveOop._list`
because it has to save each object's identifier
along with its type and its value or length.
Our `LoadAlias` class,
on the other hand,
can recycle all the loading methods for particular datatypes
from `LoadOop`.
All that has to change is the `load` method itself,
which looks to see if we're restoring aliased data
or loading something new:

[% inc file="aliasing_wrong.py" keep="load" %]

The first test of our new code is:

[% inc file="test_aliasing_wrong.py" keep="no_aliasing" %]

which uses this helper function:
{: .continue}

[% inc file="test_aliasing_wrong.py" keep="roundtrip" %]

There isn't any aliasing in the test case,
but that's deliberate:
we want to make sure we haven't broken code that was working
before we move on.
{: .continue}

Here's a test that actually includes some aliasing:

[% inc file="test_aliasing_wrong.py" keep="shared" %]

It checks that the aliased sub-list is actually aliased after the data is restored,
and then checks that modifying that sub-list works as it should
(i.e.,
that changes made through one alias are visible through the other).
The second check ought to be redundant,
but it's still comforting.
{: .continue}

There's one more case to check,
and unfortunately it turns up a bug in our code.
The two lines:

```python
fixture = []
fixture.append(fixture)
```

create the data structure shown in [%fixme persistence-circular %],
in which an object contains a reference to itself.
Our code ought to handle this case but doesn't:
when we try to read in the saved data,
`LoadAlias.load` sees the `alias` line
but then says it can't find the object being referred to.
{: .continue}

[% fixme
   slug="persistence-circular"
   img="circular.svg"
   alt="A Circular Data Structure"
   caption="FIXME"
%]

The problem is these lines in `LoadAlias.load`
marked as containing a bug,
in combination with these lines inherited from `LoadOop`:
{: .continue}

[% inc file="oop.py" keep="load_list" %]

Let's trace execution for the saved data:
{: .continue}

```
list:4484025600:1
alias:4484025600:
```

1.  The first line tells us that there's a list whose ID is `4484025600`
    so we `LoadOop._list` to load a list of one element.

1.  `LoadOop._list` called `LoadAlias.load` recursively to load that one element.

1.  `LoadAlias.load` reads the second line of saved data,
    which tells it to re-use the data whose ID is `4484025600`.
    But `LoadOop._list` hasn't created and returned that list yet—it
    is still reading in the elements—so
    `LoadAlias.load` hasn't had a chance to add the list to the `seen` dictionary
    of previously-read items.

The solution is to reorder the operations,
which unfortunately means writing new versions
of all the methods defined in `LoadOop`.
The new implementation of `_list` is:

[% inc file="aliasing.py" keep="load_list" %]

This method creates the list it's going to return,
adds that list to the `seen` dictionary immediately,
and *then* loads list items recursively.
We have to pass it the ID of the list
to use as the key in `seen`,
and we have to use a loop rather than a [%g list_comprehension "list comprehension" %],
but the changes to `_set` and `_dict` follow exactly the same pattern.

## User-Defined Classes {: #persistence-extend}

It's time to extend our framework to handle user-defined classes.
We'll start by refactoring our code so that the `save` method doesn't get any larger:

[% inc file="extend.py" keep="save" omit="omit_extension" %]

The method to handle built-in types is:
{: .continue}

[% inc file="extend.py" keep="save_builtin" %]

and the one that handles aliases is:
{: .continue}

[% inc file="extend.py" keep="save_aliased" %]

None of this code is new:
we've just moved things into methods
to make each piece easier to understand.
{: .continue}

So how does a class indicate that it can be saved and loaded by our framework?
One option would be to have it inherit from some base class;
another is just to require it to have some particular method
that gives us what we need.
The second is simpler,
so we arbitrarily decide that
if a class has a method called `to_dict`,
we'll call that to get its contents as a dictionary
and then persist the dictionary.
Before doing that,
though,
we will save a line indicating that
this dictionary should be used to reconstruct an object
of a particular class:

[% inc file="extend.py" keep="save_extension" %]

Loading user-defined classes requires more work
because we have to map class names back to actual classes.
We start by modifying the loader's constructor
to take zero or more extension classes as arguments
and then build a name-to-class lookup table from them:

[% inc file="extend.py" keep="load_constructor" %]

The `load` method then looks for aliases,
built-in types,
and extensions in that order.
Instead of using a chain of `if` statements
we loop over the methods that handle these cases.
If a method decides that it can handle the incoming data
it returns a result;
if it can't,
it throws a `KeyError`,
and if none of the methods handle a case
we fail:

[% inc file="extend.py" keep="load_load" %]

The code to handle built-ins and aliases is copied from our previous work
and modified to raise `KeyError`:

[% inc file="extend.py" keep="inherited" %]

The method that handles extensions
checks that the value on the line just read indicates an extension,
then reads the dictionary containing the object's contents
from the input stream
and uses it to build an instance of the right class:

[% inc file="extend.py" keep="load_extension" %]

Here's a class that defines the required method:

[% inc file="user_classes.py" keep="parent" %]

and here's a test to make sure everything works:

[% inc file="test_extend.py" keep="test_parent" %]

<div class="callout" markdown="1">
### What's in a name?

The first version of these classes used the word `"extension"`
rather than `"@extension"`.
That led to the most confusing bug in this whole chapter.
When `load` reads a line,
it runs `self._builtin` before running `self._extension`.
If the first word on the line is `"extension"` (without the `@`)
then `self._builtin` constructs the method name `_extension`,
finds that method,
and calls it
as if we were loading an object of a built-in type:
which we're not.
Using `@extension` as the leading indicator
leads to `self._builtin` checking for `"_@extension"` in the loader's attributes,
which doesn't exist,
so everything goes as it should.

</div>

The tools we have developed do what they're supposed to do,
but please don't ever use them in real applications:
the world already has enough data storage formats.

[% fixme concept-map %]

## Exercises {: #persistence-exercises}

### Reset {: .exercise}

`SaveAlias`, `SaveExtend`, and their loading counterparts
don't re-set the tables of objects seen so far between runs.

1.  If we construct one saver object and use it repeatedly on different data,
    can it create incorrect or misleading archives?

1.  What about loading?
    If we re-use a loader,
    can it construct objects that aren't what they should be?

1.  Create new classes `SaveReset` and `LoadReset`
    that fix the problems you have identified.
    How much of the existing code did you have to change?

### A Dangling Colon {: .exercise}

Why is there a colon at the end of the line `alias:12345678:`
when we create an alias marker?

### Versioning {: .exercise}

We now have several versions of our data storage format.
Early versions of our code can't read the archives created by later ones,
and later ones can't read the archives created early on
(which used two fields per line rather than three).
This problem comes up all the time in long-lived libraries and applications,
and the usual solution is to include some sort of version marker
at the start of each archive
to indicate what version of the software created it
(and therefore how it should be read).
Modify the code we have written so far to do this.

### Who Calculates? {: .exercise}

Why doesn't `LoadAlias.load` calculate object IDs?
Why does it use the IDs saved in the archive instead?

### Fallback {: .exercise}

1.  Modify `LoadExtend` so that
    if the user didn't provide the class needed to reconstruct some archived data,
    the `load` method returns a simple dictionary instead.

1.  Why is this a bad idea?

### Looking Around {: .exercise}

[%x tester %] introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify `LoadExtend` so that it looks for classes using `globals`
    rather than requiring the caller to pass in
    the classes it's allowed to use.

1.  Why is this a bad idea?

### Removing Exceptions {: .exercise}

Rewrite `LoadExtend` so that it doesn't use exceptions
when `_aliased`, `_builtin`, and `extension` decide
they aren't the right method to handle a particular case.
Is the result simpler or more complex than the exception-based approach?

### Self-Referential Objects {: .exercise}

Suppose an object contains a reference to itself:

```python
class Example:
    def __init__(self):
        self.ref = None

ex = Example()
ex.ref = ex
```

1.  Why can't `SaveExtend` and `LoadExtend` handle this correctly?

1.  How would they have to be changed to handle this?
