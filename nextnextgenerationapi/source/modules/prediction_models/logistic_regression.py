import numpy as np
import pandas as pd
from joblib import load  # type: ignore
from nba_api.stats.endpoints import leaguegamefinder  # type: ignore

model = load("models/logistic_regression.joblib")


def predict_games(team_home : str, team_away : str) -> tuple[int, float]:
    gamefinder = leaguegamefinder.LeagueGameFinder(
        date_from_nullable="01/01/2021", league_id_nullable="00"
    )
    games = gamefinder.get_data_frames()[0]
    games = games[["TEAM_NAME", "GAME_ID", "GAME_DATE", "MATCHUP", "WL", "PLUS_MINUS"]]
    games["GAME_DATE"] = pd.to_datetime(games["GAME_DATE"])

    msk_home = games["TEAM_NAME"] == team_home
    games_30_home = games[msk_home].sort_values("GAME_DATE").tail(30)
    home_plus_minus = games_30_home["PLUS_MINUS"].mean()

    msk_away = games["TEAM_NAME"] == team_away
    games_30_away = games[msk_away].sort_values("GAME_DATE").tail(30)
    away_plus_minus = games_30_away["PLUS_MINUS"].mean()

    games_diff = home_plus_minus - away_plus_minus

    predict_home_win = model.predict(np.array([games_diff]))[0]
    predict_winning_probability = model.predict_proba(np.array([games_diff]))[0][1]
    return predict_home_win, predict_winning_probability
