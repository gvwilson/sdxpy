"""Test improved pipeline."""

from textwrap import dedent
from unittest.mock import patch

import pandas as pd
import yaml
from pytest import fixture

from nitinat.pipeline2 import pipeline

READ_CONFIG = "nitinat.pipeline2._read_config"
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


@fixture
def available():
    return {f.__name__: f for f in [first, head, tail, reader]}


def test_pipeline2_empty_returns_nothing(available):
    with patch(READ_CONFIG, return_value=[]):
        result = pipeline("test.yml", available)
        assert result is None


def test_pipeline2_single_stage_no_parameters_no_overall(available):
    config = [{"function": "reader"}]
    with patch(READ_CONFIG, return_value=config):
        expected = simple_df()
        result = pipeline("test.yml", available)
        assert result.equals(expected)


def test_pipeline2_two_stages_with_parameters_no_overall(available):
    config = [{"function": "reader"}, {"function": "head", "num": 2}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == 2
        assert result.equals(simple_df().iloc[[0, 1]])


def test_pipeline2_single_stage_with_debugging(available):
    config = [{"function": "reader", "debug": True}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == READER_SHORTENED_LEN


def test_pipeline2_single_stage_with_overall_debugging(available):
    config = [{"overall": {"debug": True}}, {"function": "reader"}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == READER_SHORTENED_LEN


def test_pipeline2_two_stage_with_overall_debugging(available):
    config = [
        {"overall": {"debug": True}},
        {"function": "reader"},
        {"function": "head", "num": len(simple_df())},
    ]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == 1


def test_pipeline2_two_stage_with_yaml_text(available):
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
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", available)
        assert len(result) == 1
