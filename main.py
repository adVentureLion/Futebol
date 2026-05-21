from src.preprocessing.clean import run_clean
import pandas as pd
from src.features.rest_days import add_rest_days


def initial():
    df = run_clean()
    print(type(df))
    df = add_rest_days(df)

    df.to_csv("data/interim/data.csv")

    # print(df.info())

initial()





