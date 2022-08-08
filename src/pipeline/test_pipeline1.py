"""Test pipeline."""

from pathlib import Path
from unittest.mock import patch

import pandas as pd
from pytest import fixture

from nitinat.pipeline import pipeline

READ_CONFIG = "nitinat.pipeline._read_config"


@fixture
def simple_df():
    return pd.DataFrame(
        {
            "red": [0.1, 0.2, 0.3],
            "green": [0.4, 0.5, 0.6],
            "blue": [0.7, 0.8, 0.9],
        }
    )


def first(df):
    """To demonstrate pipeline operation."""
    return df.iloc[[0]]


def head(df, num):
    """To demonstrate pipeline operation."""
    return df.head(num)


def tail(df, num):
    """To demonstrate pipeline operation."""
    return df.tail(num)


def reader(df, filename):
    """To demonstrative pipeline operation."""
    assert df is None
    with open(filename, "r") as reader:
        return pd.read_csv(reader)


def test_pipeline_empty_returns_original_data(simple_df):
    config = []
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df)
        assert result.equals(simple_df)


def test_pipeline_single_stage_no_parameters(simple_df):
    config = [{"function": "first"}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df, first)
        assert len(result) == 1
        assert result.equals(simple_df.iloc[[0]])


def test_pipeline_single_stage_with_parameters(simple_df):
    config = [{"function": "head", "num": 2}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df, head)
        assert len(result) == 2
        assert result.equals(simple_df.iloc[[0, 1]])


def test_pipeline_two_stages_with_parameters(simple_df):
    config = [{"function": "head", "num": 2}, {"function": "head", "num": 1}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df, head)
        assert len(result) == 1
        assert result.equals(simple_df.iloc[[0]])


def test_pipeline_multiple_functions(simple_df):
    config = [{"function": "head", "num": 2}, {"function": "tail", "num": 1}]
    with patch(READ_CONFIG, return_value=config):
        result = pipeline("test.yml", simple_df, head, tail)
        assert len(result) == 1
        assert result.equals(simple_df.iloc[[1]])


def test_pipeline_with_real_files():
    filename = Path(__file__).parent.joinpath("simple_pipeline.yml")
    result = pipeline(filename, None, reader, head)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
