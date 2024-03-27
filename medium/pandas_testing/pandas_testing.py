import pandas as pd


def count_time_good(arg):
    print(type(arg), arg)


def sum_time():
    pass


if __name__ == '__main__':
    df = pd.DataFrame({
        "name": ["mike", "tim", "frank"],
        "start": ["13:00:05", "13:00:07", "13:01:20"],
        "finish": ["14:15:33", "14:48:29", "14:16:11"]
    })

    print(df)