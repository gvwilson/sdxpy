"""Test provenance pipeline."""

from datetime import datetime
from textwrap import dedent
from unittest.mock import patch

import pandas as pd
import yaml
from pytest import fixture

from pipeline.pipeline3 import pipeline

READ_CONFIG = "pipeline.pipeline3._read_config"
NOW = "pipeline.pipeline3._now"
READER_SHORTENED_LEN = 3


def simple_df():
    return pd.DataFrame(
        {
            "red": [0.1, 0.2, 0.3],
            "green": [0.4, 0.5, 0.6],
            "blue": [0.7, 0.8, 0.9],
            "orange": [1.1, 1.2, 1.3],
            "yellow": [1.4, 1.5, 1.6],
            "purple": [1.7, 1.8, 1.9],
        }
    )


def times(num_stages):
    return [datetime(2022, 1, 1, 1, 1, i) for i in range(2 * num_stages)]


def first(df):
    """To demonstrate pipeline operation."""
    return df.iloc[[0]]


def head(df, num, debug=False):
    """To demonstrate pipeline operation."""
    return df.head(1) if debug else df.head(num)


def tail(df, num, debug=False):
    """To demonstrate pipeline operation."""
    return df.tail(1) if debug else df.tail(num)


def reader(debug=False):
    """To demonstrate pipeline operation."""
    df = simple_df()
    return df.head(READER_SHORTENED_LEN) if debug else df


def failure(df, debug=False):
    """To demonstrate pipeline operation."""
    raise ValueError("failure message")


@fixture
def available():
    return {f.__name__: f for f in [first, head, tail, reader, failure]}


def test_pipeline3_empty_returns_nothing(available):
    with patch(READ_CONFIG, return_value=[]):
        provenance, result = pipeline("test.yml", available)
        assert result is None
        assert provenance == []


def test_pipeline3_single_stage_no_parameters_no_overall(available):
    config = [{"function": "reader"}]
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(1)),
    ):
        expected = simple_df()
        provenance, result = pipeline("test.yml", available)
        assert result.equals(expected)
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader"}
        ]


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


def test_pipeline3_single_stage_with_debugging(available):
    config = [{"function": "reader", "debug": True}]
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(1)),
    ):
        provenance, result = pipeline("test.yml", available)
        assert len(result) == READER_SHORTENED_LEN
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader", "debug": True}
        ]


def test_pipeline3_single_stage_with_overall_debugging(available):
    config = [{"overall": {"debug": True}}, {"function": "reader"}]
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(1)),
    ):
        provenance, result = pipeline("test.yml", available)
        assert len(result) == READER_SHORTENED_LEN
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader", "debug": True}
        ]


def test_pipeline3_two_stage_with_overall_debugging(available):
    data_len = len(simple_df())
    config = [
        {"overall": {"debug": True}},
        {"function": "reader"},
        {"function": "head", "num": data_len},
    ]
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(2)),
    ):
        provenance, result = pipeline("test.yml", available)
        assert len(result) == 1
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader", "debug": True},
            {
                "exc": None,
                "elapsed": 1.0,
                "function": "head",
                "num": data_len,
                "debug": True,
            },
        ]


def test_pipeline3_two_stage_with_yaml_text(available):
    config = dedent(
        """\
    - overall:
        debug: true
    - function: reader
    - function: head
      num: 1000
    """
    )
    config = yaml.safe_load(config)
    with (
        patch(READ_CONFIG, return_value=config),
        patch(NOW, side_effect=times(2)),
    ):
        provenance, result = pipeline("test.yml", available)
        assert len(result) == 1
        assert provenance == [
            {"exc": None, "elapsed": 1.0, "function": "reader", "debug": True},
            {
                "exc": None,
                "elapsed": 1.0,
                "function": "head",
                "num": 1000,
                "debug": True,
            },
        ]


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
