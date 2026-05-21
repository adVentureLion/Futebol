import pandas as pd

def add_rest_days(df):
    
    df["data"] = pd.to_datetime(df["data"])

    df["home_rest_days"] = 0
    df["away_rest_days"] = 0

    last_match_date = {}

    for idx, row in df.iterrows():

        home = row["mandante"]
        away = row["visitante"]

        current_date = row["data"]

        if home in last_match_date:

            home_rest = (current_date - last_match_date[home]).days

            df.at[idx, "home_rest_days"] = home_rest

        else:

            df.at[idx, "home_rest_days"] = None

        if away in last_match_date:

            away_rest = (current_date - last_match_date[away]).days

            df.at[idx, "away_rest_days"] = away_rest

        else:

            # primeiro jogo do time
            df.at[idx, "away_rest_days"] = None


        last_match_date[home] = current_date
        last_match_date[away] = current_date

    # transformar em numérico
    df["home_rest_days"] = pd.to_numeric(df["home_rest_days"])

    df["away_rest_days"] = pd.to_numeric(df["away_rest_days"])

    # preencher NaN
    # assumindo semana cheia de descanso
    df["home_rest_days"] = (df["home_rest_days"].fillna(7))

    df["away_rest_days"] = (df["away_rest_days"].fillna(7))

    # diferença de descanso
    df["rest_diff"] = (df["home_rest_days"] - df["away_rest_days"])

    # df.to_csv("data/interim/data.csv")

    return df
