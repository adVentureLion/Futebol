# src/models/train.py

import pandas as pd

from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


FEATURES = [

    "mandante",
    "visitante",

    "rodada",

    "elo_home",
    "elo_away",
    "elo_diff",

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
    "goal_diff_diff",

    "home_rest_days",
    "away_rest_days",
    "rest_diff",

    "season",
    "month"
]

TARGET = "time_vencedor"


CAT_FEATURES = [
    "mandante",
    "visitante"
]


def load_data():

    df = pd.read_csv(
        "data/processed/data_model.csv"
    )

    return df


def temporal_split(df):

    train_df = df[
        df["season"] <= 2022
    ]

    test_df = df[
        df["season"] == 2023
    ]

    return train_df, test_df


def prepare_data(train_df, test_df):

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    return X_train, y_train, X_test, y_test


def create_model():

    model = CatBoostClassifier(

        iterations=1000,

        learning_rate=0.03,

        depth=4,

        l2_leaf_reg=10,

        loss_function="MultiClass",

        auto_class_weights="Balanced",

        eval_metric="Accuracy",

        verbose=100
    )

    return model


def train_model(
    model,
    X_train,
    y_train,
    X_test,
    y_test
):

    model.fit(

        X_train,
        y_train,

        cat_features=CAT_FEATURES,

        eval_set=(X_test, y_test)
    )

    return model


def evaluate_model(
    model,
    X_test,
    y_test
):

    preds = model.predict(X_test)

    probs = model.predict_proba(X_test)

    acc = accuracy_score(
        y_test,
        preds
    )

    print("\n========================")
    print("ACCURACY")
    print("========================")

    print(acc)

    print("\n========================")
    print("CLASSIFICATION REPORT")
    print("========================")

    print(
        classification_report(
            y_test,
            preds
        )
    )

    print("\n========================")
    print("CONFUSION MATRIX")
    print("========================")

    print(
        confusion_matrix(
            y_test,
            preds
        )
    )


def save_model(model):

    model.save_model(
        r"C:\model\catboost_model.cbm"
    )

    print("\nModelo salvo com sucesso.")


def run_train():

    print("\nCarregando dados...")

    df = load_data()

    print("Dados carregados.")

    print("\nSeparando treino e teste...")

    train_df, test_df = temporal_split(df)

    print("Split temporal concluído.")

    print("\nPreparando datasets...")

    X_train, y_train, X_test, y_test = (
        prepare_data(
            train_df,
            test_df
        )
    )

    print("Datasets preparados.")

    print("\nCriando modelo...")

    model = create_model()

    print("Modelo criado.")

    print("\nTreinando modelo...")

    model = train_model(

        model,

        X_train,
        y_train,

        X_test,
        y_test
    )

    print("Treinamento concluído.")

    print("\nAvaliando modelo...")

    evaluate_model(
        model,
        X_test,
        y_test
    )

    print("\nSalvando modelo...")

    # save_model(model)

    print("\nProcesso finalizado.")