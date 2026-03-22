---
title: "Syllabus"
---

## [Introduction](@/intro/)

-   The complexity of a system increases more rapidly than its size.
-   The best way to learn design is to study examples, and the best programs to use as examples are the ones programmers use every day.
-   These lessons assume readers can write small programs and want to write larger ones, or are looking for material to use in software design classes that they teach.
-   All of the content is free to read and re-use under open licenses, and all royalties from sales of this book will go to charity.

## [Objects and Classes](@/oop/)

-   Objects are useful without classes, but classes make them easier to understand.
-   A well-designed class defines a contract that code using its instances can rely on.
-   Objects that respect the same contract are polymorphic, i.e., they can be used interchangeably even if they do different specific things.
-   Objects and classes can be thought of as dictionaries with stereotyped behavior.
-   Most languages allow functions and methods to take a variable number of arguments.
-   Inheritance can be implemented in several ways that differ in the order in which objects and classes are searched for methods.

## [Finding Duplicate Files](@/dup/)

-   A hash function creates a fixed-size value from an arbitrary sequence of bytes.
-   Use big-oh notation to estimate the running time of algorithms.
-   The output of a hash function is deterministic but not easy to predict.
-   A good hash function's output is evenly distributed.
-   A large cryptographic hash can be used to uniquely identify a file's contents.

## [Matching Patterns](@/glob/)

-   Use globs and regular expressions to match patterns in text.
-   Use inheritance to make matchers composable and extensible.
-   Simplify code by having objects delegate work to other objects.
-   Use the Null Object pattern to eliminate special cases in code.
-   Use standard refactorings to move code from one working state to another.
-   Build and check the parts of your code you are least sure of first to find out if your design will work.

## [Parsing Text](@/parse/)

-   Parsing transforms text that's easy for people to read into objects that are easy for computers to work with.
-   A grammar defines the textual patterns that a parser recognizes.
-   Most parsers tokenize input text and then analyze the tokens.
-   Most parsers need to implement some form of precedence to prioritize different patterns.
-   Operations like addition and function call work just like user-defined functions.
-   Programs can overload built-in operators by defining specially-named methods that are recognized by the compiler or interpreter.

## [Running Tests](@/test/)

-   Functions are objects you can save in data structures or pass to other functions.
-   Python stores local and global variables in dictionary-like structures.
-   A unit test performs an operation on a fixture and passes, fails, or produces an error.
-   A program can use introspection to find functions and other objects at runtime.

## [An Interpreter](@/interp/)

-   Compilers and interpreters are just programs.
-   Basic arithmetic operations are just functions that have special notation.
-   Programs can be represented as trees, which can be stored as nested lists.
-   Interpreters recursively dispatch operations to functions that implement low-level steps.
-   Programs store variables in stacked dictionaries called environments.
-   One way to evaluate a program's design is to ask how extensible it is.

## [Functions and Closures](@/func/)

-   When we define a function, our programming system saves instructions for later use.
-   Since functions are just data, we can separate creation from naming.
-   Most programming languages use eager evaluation, in which arguments are evaluated before a function is called.
-   Programming languages can also use lazy evaluation, in which expressions are passed to functions for just-in-time evaluation.
-   Every call to a function creates a new stack frame on the call stack.
-   When a function looks up variables it checks its own stack frame and the global frame.
-   A closure stores the variables referenced in a particular scope.

## [Protocols](@/protocols/)

-   Temporarily replacing functions with mock objects can simplify testing.
-   Mock objects can record their calls and/or return variable results.
-   Python defines protocols so that code can be triggered by keywords in the language.
-   Use the context manager protocol to ensure cleanup operations always execute.
-   Use decorators to wrap functions after defining them.
-   Use closures to create decorators that take extra parameters.
-   Use the iterator protocol to make objects work with for loops.

## [A File Archiver](@/archive/)

-   Version control tools use hashing to uniquely identify each saved file.
-   Each snapshot of a set of files is recorded in a manifest.
-   Using a mock filesystem for testing is safer and faster than using the real thing.
-   Operations involving multiple files may suffer from race conditions.
-   Use a base class to specify what a component must be able to do and derive child classes to implement those operations.

## [An HTML Validator](@/check/)

-   HTML consists of text and of elements represented by tags with attributes.
-   HTML is represented in memory as a Document Object Model (DOM) tree.
-   Trees are usually processed using recursion.
-   The Visitor design pattern is often used to perform an action for each member of a data structure.
-   We can summarize and check the structure of an HTML page by visiting each node and recording what we find there.

## [A Template Expander](@/template/)

-   Static site generators create HTML pages from templates, directives, and data.
-   A static site generator has the same core features as a programming language.
-   Special-purpose mini-languages quickly become as complex as other languages.
-   Static methods are a convenient way to group functions together.

## [A Code Linter](@/lint/)

-   A linter checks that a program conforms to a set of style and usage rules.
-   Linters typically use the Visitor design pattern to find nodes of interest in an abstract syntax tree.
-   Programs can modify a program's AST and then unparse it to create modified versions of the original program.
-   Dynamic code modification is very powerful, but the technique can produce insecure and unmaintainable code.

## [Page Layout](@/layout/)

-   A layout engine places page elements based on their size and organization.
-   Page elements are organized as a tree of basic blocks, rows, and columns.
-   The layout engine calculates the position of each block based on its size and the position of its parent.
-   Drawing blocks on top of each other is an easy way to render them.
-   Use multiple inheritance and mixin classes to inject methods into classes.

## [Performance Profiling](@/perf/)

-   Create abstract classes to specify interfaces.
-   Store two-dimensional data as rows or as columns.
-   Use reflection to match data to function parameters.
-   Measure performance to evaluate engineering tradeoffs.

## [Object Persistence](@/persist/)

-   A persistence framework saves and restores objects.
-   Persistence must handle aliasing and circularity.
-   Users should be able to extend persistence to handle objects of their own types.
-   Software designs should be open for extension but closed for modification.

## [Binary Data](@/binary/)

-   Programs usually store integers using two's complement rather than sign and magnitude.
-   Characters are usually encoded as bytes using either ASCII, UTF-8, or UTF-32.
-   Programs can use bitwise operators to manipulate the bits representing data directly.
-   Low-level compiled languages usually store raw values, while high-level interpreted languages use boxed values.
-   Sets of values can be packed into contiguous byte arrays for efficient transmission and storage.

## [A Database](@/db/)

-   Database stores records so that they can be accessed by key.
-   Log-structured database appends new records to database and invalidates older versions of records.
-   Classes are data structures that can be saved like any other data.
-   The filesystem saves data in fixed-size pages.
-   We can improve the efficiency of a database by saving records in blocks.

## [A Build Manager](@/build/)

-   Build managers track dependencies between files and update files that are stale.
-   Every build rule has a target, some dependencies, and a recipe for updating the target.
-   Build rules form a directed graph which must not contain cycles.
-   Pattern rules describe the dependencies and recipes for sets of similar files.
-   Pattern rules can use automatic variables to specify targets and dependencies in recipes.

## [A Package Manager](@/pack/)

-   Software packages often have multiple versions, which are usually identified by multi-part semantic version numbers.
-   A package manager must find a mutually-compatible set of dependencies in order to install a package.
-   Finding a compatible set of packages is equivalent to searching a multi-dimensional space.
-   The work required to find a compatible set of packages can grow exponentially with the number of packages.
-   Eliminating partially-formed combinations of packages can reduce the work required to find a compatible set.
-   An automated theorem prover can determine if a set of logical propositions can be made consistent with each other.
-   Most package managers use some kind of theorem prover to find compatible sets of packages to install.

## [Transferring Files](@/ftp/)

-   Every computer on a network has a unique IP address.
-   The Domain Name System (DNS) translates human-readable names into IP addresses.
-   Programs send and receive messages through numbered sockets.
-   The program that receives a message is responsible for interpreting the bytes in the message.
-   To test programs that rely on the network, replace the network with a mock object that simulates message transmission and receipt.

## [Serving Web Pages](@/http/)

-   The HyperText Transfer Protocol (HTTP) specifies one way to interact via messages over sockets.
-   A minimal HTTP request has a method, a URL, and a protocol version.
-   A complete HTTP request may also have headers and a body.
-   An HTTP response has a status code, a status phrase, and optionally some headers and a body.
-   HTTP is a stateless protocol: the application is responsible for remembering things between requests.

## [A File Viewer](@/viewer/)

-   The curses module manages text terminals in a platform-independent way.
-   Write debugging information to a log file when the screen is not available.
-   We can use a callable object in place of a function to satisfy an API's requirements.
-   Test programs using synthetic data.
-   Using delayed construction and/or factory methods can make code easier to evolve.
-   Refactor code before attempting to add new features.
-   Separate the logic for managing data from the logic for displaying it.

## [Undo and Redo](@/undo/)

-   Replace user interface components with mock objects to simplify testing.
-   Record actions and state to check behavior these mock objects.
-   Use objects to represent actions to record history and enable undo.
-   Recording state is easier but more expensive than recording changes.

## [A Virtual Machine](@/vm/)

-   Every computer has a processor with a particular instruction set, some registers, and memory.
-   Instructions are just numbers but may be represented as assembly code.
-   Instructions may refer to registers, memory, both, or neither.
-   A processor usually executes instructions in order but may jump to another location based on whether a conditional is true or false.

## [A Debugger](@/debugger/)

-   Interactive programs can be tested by simulating input and recording output.
-   Testing interactive programs is easier if their inputs and outputs can easily be replaced with mock objects.
-   Debuggers usually implement breakpoints by temporarily replacing actual instructions with special ones.
-   Using lookup tables for function or method dispatch makes programs easier to extend.

## [Observers](@/observe/)

-   FIXME

## [Generating Documentation](@/docgen/)

-   FIXME
-   Instructions are just numbers but may be represented as assembly code.
-   Instructions may refer to registers, memory, both, or neither.
-   A processor usually executes instructions in order but may jump to another location based on whether a conditional is true or false.

## [Search](@/search/)

-   FIXME

## [File Compression](@/compress/)

-   FIXME

## [A File Cache](@/cache/)

-   Software systems often use caches to store a subset of files in order to use less disk space.
-   Caching systems can replace actual files with placeholders containing metadata.
-   Object-oriented systems are often implemented in stages to break large design problems into smaller, more manageable ones.
-   In a good design, derived classes only have to override a few (preferably none) of the methods implemented in parent classes.
-   Implementing a minimum testable class allows early testing of core functionality.

## [A Query Builder](@/query/)

-   FIXME

## [Concurrency](@/concur/)

-   FIXME

## [Conclusion](@/finale/)

(No syllabus points defined.)
