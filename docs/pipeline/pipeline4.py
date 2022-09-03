"""Run a pipeline with layered configuration."""

from datetime import datetime
from pathlib import Path

import yaml

SYSTEM_CONFIG = "/etc/nitinat.yml"


def pipeline(config_file, available):
    """Construct and run a processing pipeline.

    Args:
        config_file (str): YAML configuration file describing pipeline.
        available (dict): name-to-function dictionary of allowed processors.

    Returns:
        - list[dict]: provenance record.
        - dataframe | None: pipeline result or `None` if error.
    """
    # Set up.
    layered = read_layered_config(config_file)
    raw_config = _read_config(config_file)
    overall, stages = split_config(raw_config)
    overall = layered | overall

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


def pre_stage(overall, stage):
    """Prepare for running a stage.

    Args:
        overall (dict): overall configuration.
        stage (dict): configuration for this stage.

    Returns:
        - str: function name
        - dict: function parameters
    """
    func_name = stage["function"]
    params = overall | stage
    del params["function"]
    return func_name, params


def run_stage(available, func_name, params, data):
    """Run a single stage, recording provenance.

    Args:
        available (dict): name-to-function dictionary of allowed processors.
        func_name (str): name of function to run.
        params (dict): named parameters for function call from pipeline config.
        data (dataframe | None): input dataframe or `None` for the first stage.

    Returns:
        - dict: full parameter set used in call.
        - dataframe | None: result of processing or `None` if error.
    """
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


def split_config(raw):
    """Split configuration into overall and per-stage.

    Args:
        raw (list[dict]): pipeline configuration.

    Returns:
        - dict: overall settings under "overall" key.
        - list[dict]: per-stage configurations.
    """
    for (i, entry) in enumerate(raw):
        if "overall" in entry:
            del raw[i]
            return entry["overall"], raw
    return {}, raw


def get_function(available, name):
    """Look up a function by name.

    Args:
        available (dict): name-to-function dictionary of allowed processors.
        func_name (str): name of function to run.

    Returns:
        callable: the desired function.

    Raises:
        AssertionError: if the desired function isn't available.
    """
    assert name in available
    return available[name]


def read_layered_config(config_file):
    """Read layered configuration files in order."""
    all_filenames = [SYSTEM_CONFIG, _get_home_dir().joinpath(".nitinat.yml")]
    if project_config := _find_project_config(config_file):
        all_filenames.append(project_config)
    config = {}
    for filename in all_filenames:
        if Path(filename).exists():
            config |= _read_config(filename)
    return config


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


def _get_home_dir():  # pragma: no cover
    """Get current user's home directory."""
    return Path.home()


def _now():
    """Get current time."""
    return datetime.now()


def _read_config(filename):  # pragma: no cover
    """Read YAML configuration file."""
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
