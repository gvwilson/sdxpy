"""Run a pipeline with configuration."""

import yaml


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


def split_config(raw):
    """Split configuration into overall and per-stage."""
    for (i, entry) in enumerate(raw):
        if "overall" in entry:
            del raw[i]
            return entry["overall"], raw
    return {}, raw


def get_function(available, name):
    """Look up a function by name."""
    assert name in available
    return available[name]


def _read_config(filename):  # pragma: no cover
    """Read YAML configuration file."""
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
