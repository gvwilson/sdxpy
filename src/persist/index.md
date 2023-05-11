## Exercises {: #persist-exercises}

### Using Globals {: .exercise}

The lesson on unit testing introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify the persistence framework so that it looks for `save_` and `load_` functions using `globals`.

1.  Why is this a bad idea?

### Aliasing {: .exercise}

1.  Read the section on aliasing.

2.  Modify the functions to handle aliases.
    (You may need to give the `save_*` and `load_*` functions another parameter
    to keep track of the objects seen so far.)

### Strings {: .exercise}

Modify the framework so that strings are stored using escape characters like `\n`
instead of being split across several lines.
