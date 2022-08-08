---
title: "A Pipeline Runner"
syllabus:
- FIXME
---

-   Want reproducible data processing pipelines with a "test run" option
    -   Several moving parts, so do it in steps
-   We could write this:

```python
start = pd.read_csv("input.csv")
result = third(second(first(start)))
result.to_csv("output.csv")
```

-   But if we have parameters it becomes:

```python
start = pd.read_csv("input.csv")
result = third(second(first(start, alpha), beta, gamma), delta, epsilon)
result.to_csv("output.csv")
```

-   Quick, which function is getting `delta` as a parameter?
-   And how does someone reproduce this without reading the history of your GitHub repo?

## Lists of Functions {: #pipeline-funclist}

-   Break it down to more readable steps:

```python
data = pd.read_csv("input.csv")
data = first(data, alpha)
data = second(data, beta, gamma)
data = third(data, delta, epsilon)
data.to_csv("output.csv")
```

-   But a function is just another kind of object, so we can put it in a list...
-   ...and we can spread keyword arguments in a call using `*`

```python
pipeline = [
    [first, alpha],
    [second, beta, gamma],
    [third, delta, epsilon]
]
data = pd.read_csv("input.csv")
for step in pipeline:
    func, params = step[0], step[1:]
    data = func(data, *params)
data.to_csv("output.csv")
```

## Configuration {: #pipeline-config}

-   Every function remembers the name it was given when it was defined

```python
def proof(x, y):
    pass
print(proof.__name__)
#> proof
```

-   So we can convert a list of functions into a lookup table

```python
def make_table(*functions):
    return {f.__name__: f for f in functions}

def left(): pass
def right(): pass

table = make_table(left, right)
print(table)
#> {'left': <function left at 0x101a3bdc0>, 'right': <function right at 0x101a3bee0>}
```

-   Which means we should be able to run a pipeline from a YAML file that looks like this:

```yaml
- function: left
  count: 3
- function: right
  size: 0.9
```

-   Here's the code:

```python
def pipeline(config_file, data, *functions):
    """Construct and run a processing pipeline."""
    # Set up.
    config = _read_config(config_file)
    functions = {f.__name__: f for f in functions}

    # Run each stage in turn.
    for stage in config:
        func = functions[stage["function"]]
        params = {key: stage[key] for key in stage if key != "function"}
        data = func(data, **params)

    # Return final result.
    return data

def _read_config(filename):
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
```

-   Read the YAML configuration file (in a separate function so we can replace it for testing)
-   Create a lookup table from function name to function
    -   `pipeline` has been given the functions it's allowed to call
-   For each stage in the configuration file:
    -   Find the function in the lookup table
    -   Assemble the parameters in a dictionary (rather than a list) *without* the function name
    -   Call the function with the current data
    -   Return the final result

-   Here are three functions we can use to test this:

```python
def first(df):
    return df.iloc[[0]]

def head(df, num):
    return df.head(num)

def tail(df, num):
    return df.tail(num)
```

-   Yes, they're trivial, but we *want* trivial for testing
-   Let's create a simple dataframe for testing:

```python
@fixture
def simple_df():
    return pd.DataFrame({
        "red": [0.1, 0.2, 0.3],
        "green": [0.4, 0.5, 0.6],
        "blue": [0.7, 0.8, 0.9]
    })
```

-   An empty pipeline should just return the original data

```python
READ_CONFIG = "nitinat.pipeline._read_config"

def test_pipeline_empty_returns_original_data(simple_df):
    config = []
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df)
        assert result.equals(simple_df)
```

-   Here's a more complex pipeline:

```python
def test_pipeline_multiple_functions(simple_df):
    config = [
        {"function": "head", "num": 2},
        {"function": "tail", "num": 1}
    ]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df, head, tail)
        assert len(result) == 1
        assert result.equals(simple_df.iloc[[1]])
```

-   One more test: configuration file and data file on disk

-   Add a reader function
    -   Must be the first in the pipeline, so incoming dataframe must be `None`

```python
def reader(df, filename):
    """To demonstrative pipeline operation."""
    assert df is None
    with open(filename, "r") as reader:
        return pd.read_csv(reader)
```

-   Write a configuration file

```yaml
- function: reader
  filename: three-colors.csv
- function: head
  num: 1
```

-   Create the data file

```
red,green,blue
0.1,0.4,0.7
0.2,0.5,0.8
0.3,0.6,0.9
```

-   Write the test

```python
def test_pipeline_with_real_files():
    filename = Path(__file__).parent.joinpath("simple-pipeline.yml")
    result = pipeline(filename, None, reader, head)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
```

-   Again, the special variable `__file__` holds the full path of this file
    -   Its parent is the directory that contains it
    -   So the complicated `Path` expression gets `simple-pipeline.yml` in the current directory
-   Run this: it fails

```
FileNotFoundError: [Errno 2] No such file or directory: 'three-colors.csv'
```

-   Problem is that the current working directory when we run tests is the root directory of the project
    -   And our file is in `tests/three-colors.csv`, not `./three-colors.csv`
-   Temporary solution: modify the configuration file

```yaml
- function: reader
  filename: tests/three-colors.csv
- function: head
  num: 1
```

-   Now the test runs

## Global Configuration {: #pipeline-global}

-   We want global configuration (passed to all stages) as well as local (per-stage)
    -   I.e., a configuration file like this:

```yaml
- overall:
    debug: true
- function: reader
- function: head
  num: 1000
```

-   Would also prefer not to have to pass in all the needed functions separately
-   And requiring `reader` to take `None` as the first parameter seems clumsy
    -   Listen to our code
-   [%g tdd "Test-driven development" %] (TDD) doesn't actually improve productivity [%b Fucci2016 %]
    -   But working backwards from a test you have can be a good way to *explain* a design
-   Eventually wrote this:

```python
def test_pipeline2_two_stage_with_yaml_text(available):
    config = dedent("""\
    - overall:
        debug: true
    - function: reader
    - function: head
      num: 1000
    """)
    config = yaml.safe_load(config)
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == 1
```

-   The `available` fixture is a dictionary of functions the pipeline can use
    -   `textwrap.dedent` moves text back to the left margin
        -   So this is what our YAML configuration file would look like
    -   The new `pipeline` function always starts with a reader
        -   That's probably too far the other way
    -   The global `debug` flag overrides the `num` setting in `head`:

```python
def head(df, num, debug=False):
    """To demonstrate pipeline operation."""
    return df.head(1) if debug else df.head(num)
```

-   `debug` has a default value so we don't have to provide it every time
-   The revised `pipeline` function is:

```python
def pipeline(config_file, available):
    """Construct and run a processing pipeline."""
    # Set up.
    raw_config = _read_config(config_file)
    overall, stages = split_config(raw_config)

    # Run each stage in turn.
    data = None
    for stage in stages:
        func = get_function(available, stage["function"])
        params = overall | {k: stage[k] for k in stage if k != "function"}
        data = func(**params) if (data is None) else func(data, **params)

    # Return final result.
    return data
```

-   Read the configuration file
    -   Again, keep this in a separate function for easy mocking
-   Split the configuration into overall and per-stage
-   Initially have no data
-   For each stage:
    -   Get the function
    -   Construct parameters: per-stage overrides overall
    -   Call the function with data if we have any or with nothing if we don't
-   Splitting the configuration is straightforward:

```python
def split_config(raw):
    """Split configuration into overall and per-stage."""
    for (i, entry) in enumerate(raw):
        if "overall" in entry:
            del raw[i]
            return entry["overall"], raw
    return {}, raw
```

-   OK, I lied: it took a couple of tries to come up with this
    -   The overall configuration is a dictionary with one key ("overall")
-   Getting the function is straightforward:

```python
def get_function(available, name):
    """Look up a function by name."""
    assert name in available
    return available[name]
```

-   Could move this inline
    -   But it's likely to become more complicated...
    -   ...and we're going to want to add better error handling than a simple `assert`
    -   Experience (i.e., past difficulties) tell us when to plan and design ahead
-   Lots here to test, but one key feature is that we can debug individual stages:

```python
READER_SHORTENED_LEN = 3

def reader(debug=False):
    """To demonstrate pipeline operation."""
    df = simple_df()
    return df.head(READER_SHORTENED_LEN) if debug else df

def test_pipeline2_single_stage_with_debugging(available):
    config = [{"function": "reader", "debug": True}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == READER_SHORTENED_LEN
```

-   Test code should be written as cleanly as production code
    -   Which is why this code now has `READER_SHORTENED_LEN`
    -   Because an earlier version of the just used the number 3...
    -   ...which stopped working when we changed it in one place but not another
-   One final step: `inv coverage`
    -   Tells us that `_read_config` isn't being tested
    -   Could add a test that reads from an actual file...
    -   ...or add a directive in a specially-formatted comment telling coverage not to worry about it

```python
def _read_config(filename):  # pragma: no cover
    """Read YAML configuration file."""
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
```

-   Please use these sparingly

## Provenance {: #pipeline-provenance}

-   We want to know what each run of a pipeline actually did
    -   Automatically record functions and their parameters in a structured way
    -   Would also like to introduce a little error handling
-   Rewrite `pipeline` to capture functions' parameters:

```python
def pipeline(config_file, available):
    """Construct and run a processing pipeline."""
    # Set up.
    raw_config = _read_config(config_file)
    overall, stages = split_config(raw_config)

    # Run each stage in turn.
    data = None
    provenance = []
    for stage in stages:
        func_name, params = pre_stage(overall, stage)
        record, data = run_stage(available, func_name, params, data)
        provenance.append(record)
        if record["exc"] is not None:
            return provenance, None

    # Return final result.
    return provenance, data
```

-   Convert overall configuration and stage configuration into function name and parameters
    -   Run that stage, getting a record of what happened and the data to pass on
    -   Save that record
    -   If an exception occurred, stop the pipeline
    -   Only return data if the pipeline ran to the end
-   Getting the function name and parameters is just dictionary juggling:

```python
def pre_stage(overall, stage):
    """Get function, parameters, and provenance record."""
    func_name = stage["function"]
    params = overall | stage
    del params["function"]
    return func_name, params
```

-   Running the stage:

```python
def run_stage(available, func_name, params, data):
    """Run a single stage, recording provenance."""
    func = get_function(available, func_name)
    try:
        start = _now()
        data = func(**params) if (data is None) else func(data, **params)
        params["exc"] = None
    except Exception as exc:
        params["exc"] = repr(exc)
    finally:
        params["elapsed"] = (_now() - start).total_seconds()
        params["function"] = func_name
    return params, data
```

-   Steps:
    -   Look up the function
    -   Record a start time
    -   Call the function
    -   If an exception occurred, save it
    -   *Always* record the end time and the function name
-   Updating the tests

```python
def test_pipeline3_two_stages_with_parameters_no_overall(available):
    config = [{"function": "reader"}, {"function": "head", "num": 2}]
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(2)),
    ):
        provenance, result = pipeline("test.yml", available)
        assert len(result) == 2
        assert result.equals(simple_df().iloc[[0, 1]])
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader"},
            {"exc": None, "elapsed": 1.0, "function": "head", "num": 2},
        ]
```

-   Need a helper function `times` to generate predictable times

```python
NOW = "nitinat.pipeline3._now"

def times(num_stages):
    return [datetime(2022, 1, 1, 1, 1, i) for i in range(2 * num_stages)]
```

-   Always test error handling

```python
def test_pipeline3_two_stages_with_failure(available):
    config = [{"function": "reader"}, {"function": "failure"}]
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(2)),
    ):
        provenance, result = pipeline("test.yml", available)
        assert result is None
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader"},
            {
                "exc": "ValueError('failure message')",
                "elapsed": 1.0,
                "function": "failure",
            },
        ]
```

-   Note that `run_stage` converts exceptions to strings using `repr`
    -   Python doesn't implement `==` on exception objects
    -   And `str(exc)` produces the error message, not the exception class
    -   Once again, we are designing for testability

## Configuration {: #pipeline-configuration}

-   Current configuration syntax allows one "overall" section and one section per pipeline stage
-   What if we want to share the overall configuration between multiple pipelines?
-   Or share some settings for a particular stage across all uses of that stage?
-   Use a layered configuration that takes configuration in this order:
    1.  A system-wide configuration file for general settings.
    2.  A user-specific configuration file for personal preferences.
    3.  Project-specific files.
    4.  Analysis-specific files.
    5.  Command-line arguments.
-   Each level adds to or overrides settings in the layer before it
    -   Example: `.gitignore` files
-   First step: modify `pipeline`

```python
SYSTEM_CONFIG = "/etc/nitinat.yml"


def pipeline(config_file, available):
    """Construct and run a processing pipeline.""
    # Set up.
    layered = read_layered_config(config_file)
    raw_config = _read_config(config_file)
    overall, stages = split_config(raw_config)
    overall = layered | overall

    # Run each stage in turn.
    # ...as before...

    # Return final result.
    return provenance, data
```

-   Write the function to read and overlay several configuration files
    -   Yes, we've used the `:=` operator - we're sinners...

```python
def read_layered_config(config_file):
    """Read layered configuration files in order."""
    all_filenames = [SYSTEM_CONFIG, _get_home_dir().joinpath(".nitinat.yml")]
    if (project_config := _find_project_config(config_file)):
        all_filenames.append(project_config)
    config = {}
    for filename in all_filenames:
        if Path(filename).exists():
            config |= _read_config(filename)
    return config
```

-   Now look for the project configuration file
    -   Search up from the directory containing the file specified for the run
    -   Stop at the user's home directory
    -   Might be better to stop at the root of the Git repository?

```python
def _find_project_config(starting_point):
    """Look up from given file to find project configuration file."""
    curdir = Path(starting_point).resolve().parent
    home = _get_home_dir()
    while curdir > home:
        candidate = curdir.joinpath(".nitinat.yml")
        if candidate.exists():
            return candidate
        curdir = curdir.parent
    return None
```

-   Relies on a helper function `_get_home_dir`
    -   Originally just used `Path.home()`
    -   But discovered we need to patch this when testing

```python
def _get_home_dir():  # pragma: no cover
    """Get current user's home directory."""
    return Path.home()
```

-   To test:
    -   Patch `_read_config` with a sequence of return values (one per config file)
    -   Replace the entire file system
-   Install [pyfakefs][pyfakefs]
    -   Add it to `development.txt`, not `requirements.txt`
-   Use the `fs` fixture it provides to manipulate an in-memory filesystem
    -   Functions like `open` are patched behind the scenes to use it

```python
from nitinat.pipeline4 import SYSTEM_CONFIG, read_layered_config

GET_HOME_DIR = "nitinat.pipeline4._get_home_dir"


def make_file(fs, path, contents):
    fs.create_file(path, contents=yaml.dump(contents))


def test_layered_config_read_system(fs):
    fs.cwd = "/home/person/project/analysis"
    expected = {"alpha": 1}
    make_file(fs, SYSTEM_CONFIG, expected)
    with patch(GET_HOME_DIR, return_value=Path("/home/person")):
        actual = read_layered_config("test.yml")
    assert actual == expected
```

-   Line by line, `test_layered_config_read_system`:
    1.  Is given the `fs` fixture created by `pyfakefs`
    2.  Specifies the pretended current working directory
    3.  Creates the expected configuration as a dictionary
    4.  Calls `make_file` to turn that dictionary into a file in the fake filesystem
        -   `make_file` uses `fs.create_file`
        -   Pulling this out into a one-line function makes the tests easier to read
    5.  Patch the `_get_home_dir` helper function to return the right value
    6.  Reads the layered configuration
        -   Which should get just the system-wide configuration
    7.  Checks
-   Here's a test of multiple configuration files layering correctly:

```python
def test_layered_config_combine_files(fs):
    fs.cwd = "/home/person/project/analysis"
    make_file(fs, SYSTEM_CONFIG, {"alpha": 1})
    make_file(fs, "/home/person/.nitinat.yml", {"beta": 2})
    make_file(fs, "/home/person/project/.nitinat.yml", {"gamma": 3})
    with patch(GET_HOME_DIR, return_value=Path("/home/person")):
        actual = read_layered_config("temp/test.yml")
    assert actual == {"alpha": 1, "beta": 2, "gamma": 3}
```

-   Everything else in the pipeline code stays the same
-   So the provenance record for each stage has the complete configuration
    -   We really should write at least a couple of tests for that...
