import pandas as pd

initial_elo = 1500
k_factor = 15
home_advantage = 40



# Calcula a força do time B comparado ao time A
def expected_results(elo_a, elo_b):
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))


# Atualiza o elo baseado no resultado encontrado e o resultado previsto
def update_elo(current_elo, expected, actual):
    return current_elo + k_factor * (actual - expected)


# Calcula o Elo Ratings dos times e atualiza no dataFrame em ordem cronológica
# Existe um soft reset todo inicio de temporada
def add_elo_ratings(df):

    df["data"] = pd.to_datetime(df["data"], dayfirst=True)

    df = (df.sort_values("data").reset_index(drop=True))

    teams = pd.concat([df["mandante"],df["visitante"]]).unique()

    elo_dict = {team: initial_elo for team in teams}

    current_season = None

    for idx, row in df.iterrows():

        season = row["season"]

        if current_season is None:

            current_season = season

        elif season != current_season:

            for team in elo_dict:

                elo_dict[team] = (0.65 * elo_dict[team] + 0.35 * initial_elo)

            current_season = season

        home = row["mandante"]
        away = row["visitante"]

        home_elo = elo_dict[home]
        away_elo = elo_dict[away]

        df.at[idx, "elo_home"] = home_elo
        df.at[idx, "elo_away"] = away_elo

        df.at[idx, "elo_diff"] = (
            home_elo - away_elo
        )

        adjusted_home_elo = (
            home_elo + home_advantage
        )

        expected_home = expected_results(
            adjusted_home_elo,
            away_elo
        )

        expected_away = 1 - expected_home

        if row["time_vencedor"] == 1:

            actual_home = 1
            actual_away = 0

        elif row["time_vencedor"] == 2:

            actual_home = 0
            actual_away = 1

        else:

            actual_home = 0.5
            actual_away = 0.5

        new_home_elo = update_elo(
            current_elo=home_elo,
            expected=expected_home,
            actual=actual_home
        )

        new_away_elo = update_elo(
        current_elo=away_elo,
        expected=expected_away,
        actual=actual_away
        )

        elo_dict[home] = new_home_elo
        elo_dict[away] = new_away_elo

    return df


