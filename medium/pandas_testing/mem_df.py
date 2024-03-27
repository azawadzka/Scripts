import pandas as pd


def modify_df(in_df: pd.DataFrame) -> pd.DataFrame:
    print(2, id(in_df))
    in_df["name_cap"] = in_df["name"].str.title()
    print(3, id(in_df))
    return in_df

if __name__ == '__main__':
    df = pd.DataFrame({"name": ["bert", "albert"]})
    print(1, id(df))
    # modify_df(df)
    df = modify_df(df)
    print(4, id(df))
    print(df)

