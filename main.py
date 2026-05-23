from src.preprocessing.clean import run_clean
import pandas as pd
from src.features.rest_days import add_rest_days
from src.features.elo import add_elo_ratings
from src.features.last_5 import add_recent_features
from src.models.train import run_train


def initial():
    df = run_clean()

    df = add_rest_days(df)

    df = add_elo_ratings(df)

    df = add_recent_features(df)

    model_df = df.drop(columns=["hora"])

    df.to_csv("data/interim/data.csv", index=False)

    model_df.to_csv("data/processed/data_model.csv", index=False)

    # print(df.info())


def Train_Model():
    run_train()

initial()
Train_Model()





