"""Run a pipeline."""

import yaml


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
    """Read YAML configuration file."""
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
