from src.preprocessing.clean import run_clean
import pandas as pd
from src.features.rest_days import add_rest_days
from src.features.elo import add_elo_ratings


def initial():
    df = run_clean()
    df = add_rest_days(df)
    df = add_elo_ratings(df)

    df.to_csv("data/interim/data.csv")

    print(df.info())

initial()





