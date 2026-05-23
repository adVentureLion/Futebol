import pandas as pd


def create_long_df(df):
    # Mandante
    home_df = pd.DataFrame({

        "ID": df["ID"],

        "data": df["data"],
        "season": df["season"],

        "team": df["mandante"],
        "opponent": df["visitante"],

        "goals_for": df["mandante_Placar"],
        "goals_against": df["visitante_Placar"],

        "is_home": 1
    })
    # Visitande
    away_df = pd.DataFrame({

        "ID": df["ID"],

        "data": df["data"],
        "season": df["season"],

        "team": df["visitante"],
        "opponent": df["mandante"],

        "goals_for": df["visitante_Placar"],
        "goals_against": df["mandante_Placar"],

        "is_home": 0
    })

    # Concatenar
    long_df = pd.concat([
        home_df,
        away_df
    ])

    # ordenar
    long_df = (
        long_df
        .sort_values("data")
        .reset_index(drop=True)
    )

    return long_df


def add_recent_features(df):

    df["data"] = pd.to_datetime(
        df["data"],
        dayfirst=True
    )

  

    long_df = create_long_df(df)

    long_df["points"] = 0

    # vitória
    long_df.loc[
        long_df["goals_for"]
        > long_df["goals_against"],
        "points"
    ] = 3

    # empate
    long_df.loc[
        long_df["goals_for"]
        == long_df["goals_against"],
        "points"
    ] = 1

    # VITÓRIA / DERROTA

    long_df["win"] = (
        long_df["goals_for"]
        > long_df["goals_against"]
    ).astype(int)

    long_df["loss"] = (
        long_df["goals_for"]
        < long_df["goals_against"]
    ).astype(int)

    # ROLLING FEATURES

    # pontos últimos 5
    long_df["points_last5"] = (

        long_df
        .groupby("team")["points"]

        .transform(
            lambda x:
            x.shift(1)
             .rolling(5, min_periods=1)
             .mean()
        )
    )

    # vitórias últimos 5
    long_df["wins_last5"] = (

        long_df
        .groupby("team")["win"]

        .transform(
            lambda x:
            x.shift(1)
             .rolling(5, min_periods=1)
             .sum()
        )
    )

    # gols feitos últimos 5
    long_df["goals_scored_last5"] = (

        long_df
        .groupby("team")["goals_for"]

        .transform(
            lambda x:
            x.shift(1)
             .rolling(5, min_periods=1)
             .mean()
        )
    )

    # gols sofridos últimos 5
    long_df["goals_conceded_last5"] = (

        long_df
        .groupby("team")["goals_against"]

        .transform(
            lambda x:
            x.shift(1)
             .rolling(5, min_periods=1)
             .mean()
        )
    )

    # saldo últimos 5
    long_df["goal_diff_last5"] = (
        long_df["goals_scored_last5"]
        - long_df["goals_conceded_last5"]
    )

    # HOME FEATURES

    home_features = long_df[
        long_df["is_home"] == 1
    ].copy()

    home_features = home_features.rename(columns={

        "points_last5":
            "home_points_last5",

        "wins_last5":
            "home_wins_last5",

        "goals_scored_last5":
            "home_goals_scored_last5",

        "goals_conceded_last5":
            "home_goals_conceded_last5",

        "goal_diff_last5":
            "home_goal_diff_last5"
    })

    # AWAY FEATURES

    away_features = long_df[
        long_df["is_home"] == 0
    ].copy()

    away_features = away_features.rename(columns={

        "points_last5":
            "away_points_last5",

        "wins_last5":
            "away_wins_last5",

        "goals_scored_last5":
            "away_goals_scored_last5",

        "goals_conceded_last5":
            "away_goals_conceded_last5",

        "goal_diff_last5":
            "away_goal_diff_last5"
    })

    # COLUNAS NECESSÁRIAS

    home_features = home_features[[
        "ID",

        "home_points_last5",
        "home_wins_last5",
        "home_goals_scored_last5",
        "home_goals_conceded_last5",
        "home_goal_diff_last5"
    ]]

    away_features = away_features[[
        "ID",

        "away_points_last5",
        "away_wins_last5",
        "away_goals_scored_last5",
        "away_goals_conceded_last5",
        "away_goal_diff_last5"
    ]]

    # MERGE HOME

    df = df.merge(
        home_features,
        on="ID",
        how="left"
    )

    # MERGE AWAY

    df = df.merge(
        away_features,
        on="ID",
        how="left"
    )

    # FEATURES DE DIFERENÇA

    df["points_diff_last5"] = (
        df["home_points_last5"]
        - df["away_points_last5"]
    )

    df["goal_diff_diff"] = (
        df["home_goal_diff_last5"]
        - df["away_goal_diff_last5"]
    )

    # PREENCHER NaN

    rolling_cols = [

        "home_points_last5",
        "away_points_last5",

        "home_wins_last5",
        "away_wins_last5",

        "home_goals_scored_last5",
        "away_goals_scored_last5",

        "home_goals_conceded_last5",
        "away_goals_conceded_last5",

        "home_goal_diff_last5",
        "away_goal_diff_last5",

        "points_diff_last5",
        "goal_diff_diff"
    ]

    df[rolling_cols] = (
        df[rolling_cols]
        .fillna(0)
        .astype(float)
    )

    return df