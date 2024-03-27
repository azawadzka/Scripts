from typing import Collection, Optional

import pandas as pd
import pytest


def find_max_name_length(df: pd.DataFrame) -> int:
    df["name_len"] = df["name"].str.len()  # side effect
    return max(df["name_len"])


@pytest.mark.parametrize("df, result", [
    (pd.DataFrame({"name": []}), 0),  # oops, this fails!
    (pd.DataFrame({"name": ["bert"]}), 4),
    (pd.DataFrame({"name": ["bert", "roberta"]}), 7),
])
def test_find_max_name_length(df: pd.DataFrame, result: int):
    assert find_max_name_length(df) == result


def find_max_element(collection: Collection) -> int:
    return max(collection) if len(collection) else 0


@pytest.mark.parametrize("collection, result", [
    ([], 0),
    ([4], 4),
    ([4, 7], 7),
    (pd.Series([4, 7]), 7),
])
def test_find_max_element(collection: Collection, result):
    assert find_max_element(collection) == result


def create_name_len_col(series: pd.Series) -> pd.Series:
    return series.str.len()

@pytest.mark.parametrize("series1, series2", [
    (pd.Series([]), pd.Series([])),
    (pd.Series(["bert"]), pd.Series([4])),
    (pd.Series(["bert", "roberta"]), pd.Series([4, 7]))
])
def test_create_name_len_col(series1: pd.Series, series2: pd.Series):
    pd.testing.assert_series_equal(create_name_len_col(series1), series2, check_dtype=False)


def compute_length(word: Optional[str]) -> int:
    return len(word) if word else 0

@pytest.mark.parametrize("word, length", [
    ("", 0),
    ("bert", 4),
    (None, 0)
])
def test_compute_length(word: str, length: int):
    assert compute_length(word) == length