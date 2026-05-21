import pandas as pd

def main():
    df = pd.read_csv(r"data\raw\campeonato-brasileiro-full.csv", sep=";")
    df = clean(df)
    df = features(df)
    df.to_csv("data/processed/data_full.csv")

def clean(df):

    df = df.drop(columns=["Unnamed: 10"])
    df = df.drop(columns=["Unnamed: 11"])

    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["hora"] = pd.to_datetime(df["hora"], format="%H:%M").dt.time

    df = df.sort_values("data")

    df.to_csv("data/interim/clean_data.csv")

    return df


def features(df):
    df["elo_home"] = 0.0
    df["elo_away"] = 0.0
    df["elo_diff"] = 0.0
    df["home_points_last5"] = 0
    df["away_points_last5"] = 0
    df["home_wins_last5"] = 0
    df["away_wins_last5"] = 0
    df["home_goals_scored_last5"] = 0
    df["away_goals_scored_last5"] = 0
    df["home_goals_conceded_last5"] = 0
    df["away_goals_conceded_last5"] = 0
    df["home_goal_diff_last5"] = 0
    df["away_goal_diff_last5"] = 0
    df["points_diff_last5"] = df["home_points_last5"] - df["away_goals_scored_last5"]
    df["goal_diff_diff"] = df["home_goals_scored_last5"] - df["away_goals_scored_last5"]
    df["season"] = df["data"].dt.year
    
    return df
    

main()