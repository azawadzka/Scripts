from typing import Container

import pandas as pd


def find_max_name_length_1(df: pd.DataFrame) -> int:
    df["name_len"] = df["name"].str.len()  # side effect
    return max(df["name_len"])

def find_max_name_length_2(df: pd.DataFrame) -> int:
    lengths: pd.Series = df["name"].str.len()
    return max(lengths)

def find_max_element(container: Container) -> int:
    return max(container) if len(container) else 0

def create_name_len_col(series: pd.Series) -> pd.Series:
    return series.str.len().rename("name_len")

def create_name_len_col_2(df: pd.DataFrame, orig_col: str, target_col: str) -> pd.Series:
    return df[orig_col].str.len().rename(target_col)

def compute_length(word: str) -> int:
    return len(word)

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([
        df.copy(deep=True),  # deep copy
        df.name.apply(compute_length).rename("name_len")
    ], axis=1)

def max_name_length(str):
    return len(str)


if __name__ == '__main__':
    ## Output arguments
    # df = pd.DataFrame({"name": ["bert", "albert"]})
    # max_name_length = find_max_name_length_1(df)
    # max_name_length = find_max_name_length_2(df)
    # print(max_name_length)
    # print(df)

    ## Reduce modifications
    # df = pd.DataFrame({"name": ["bert", "albert"]})
    # series = df["name"]     # shallow copy
    # series[0] = "roberta"   # <-- this changes the original DataFrame
    # print(df)
    #
    # df = pd.DataFrame({"name": ["bert", "albert"]})
    # series = df["name"].copy(deep=True)
    # series[0] = "roberta"   # <-- this doesn't change the original DataFrame
    # print(df)

    # Group similar operations
    # df = pd.DataFrame({"name": ["bert", "albert"]})
    # df = pd.concat([
    #     df,
    #     create_name_len_col(df.name),
    #     df.name.apply(len).rename("name_len")
    # ], axis=1)

    # Group similar operations
    df = pd.DataFrame({"name": ["bert", "albert"]})
    df["name_len"] = create_name_len_col(df.name)
    print(df)

    ##
    # df = pd.DataFrame({"name": ["bert", "albert"]})
    # s1 = create_name_len_col_2(df, "name", "name_len")
    # print(s1)

    # df = pd.DataFrame({"name": ["bert", "albert"]})
    # df = prepare_data(df)
    # print(df)

