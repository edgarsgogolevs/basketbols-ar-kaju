import numpy as np
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder  # type: ignore
from typing import Any, Union
import logging
import time
from os import environ

import modules.models as models
from modules.db import Db
import modules.models as models
import modules.teams as teams

PROXY = environ.get("NBA_PROXY")
DATE_FROM = "01/01/2021"
NBA_LEAGUE_ID = "00"
GAMES_UPDATE_INTERVAL = 60 * 2  # 2 minutes

lg = logging.getLogger("modules.predict")
db = Db()
last_req = 0.0
game_finder = None
data_frames : Union[None, list] = None

def predict_game_by_game_id_model_id(
        game_id: int,
        model_id: int,
        save_prediction=True) -> Union[dict, None]:
    # Check if prediction already exists
    existing_prediction = db.select(
        "SELECT game_id, model_id, home_wins, home_winning_proba, prediction_correct FROM basketball.game_predictions WHERE game_id=? AND model_id=?",
        (game_id, model_id),
    )
    if existing_prediction:
        lg.info("Prediction already exists")
        return existing_prediction[0]

    game_data = db.select("SELECT * FROM basketball.games WHERE id=?",
                          (game_id, ))
    lg.info("game data: %s", game_data)
    if not game_data:
        return None

    game_data = game_data[0]
    team_home_id = game_data["team_home"]
    team_away_id = game_data["team_away"]
    team_home_name = teams.get_team_name_by_id(team_home_id)
    team_away_name = teams.get_team_name_by_id(team_away_id)
    model = models.MODEL_ID_TO_MODEL_MAPPING.get(model_id)
    predict_home_win, predict_winning_probability = generate_prediction(
        model, team_home_name, team_away_name)
    ret = {
        "game_id": game_id,
        "model_id": model_id,
        "home_wins": int(predict_home_win),
        "home_winning_proba": float(predict_winning_probability),
    }
    game_info = db.select(
        "SELECT team_home, team_away, home_won FROM basketball.games WHERE id=?",
        (game_id, ))[0]
    if game_info["home_won"] is not None:
        if game_info["home_won"] == ret["home_wins"]:
            ret["prediction_correct"] = True
        else:
            ret["prediction_correct"] = False
    if save_prediction:
        db.insert_dict("basketball.game_predictions", ret)
    if game_info:
        ret["team_home_id"] = game_info["team_home"]
        ret["team_away_id"] = game_info["team_away"]
    return ret

def update_game_finder() -> None:
    global game_finder, last_req, data_frames
    if game_finder and time.time() - last_req < GAMES_UPDATE_INTERVAL:
        return
    kwargs = {
        "date_from_nullable": DATE_FROM,
        "league_id_nullable": NBA_LEAGUE_ID
    }
    if PROXY:
        lg.info(f"Using proxy: {PROXY}")
        kwargs["proxy"] = PROXY
    game_finder = leaguegamefinder.LeagueGameFinder(**kwargs)
    last_req = time.time()
    data_frames = game_finder.get_data_frames()

def generate_prediction(model: Any, team_home: str,
                        team_away: str) -> tuple[int, float]:
    global data_frames
    if time.time() - last_req < 0.6:
        time.sleep(0.6)
    update_game_finder()
    if data_frames is None:
        raise Exception("No data frames")
    games = data_frames[0]
    games = games[[
        "TEAM_NAME", "GAME_ID", "GAME_DATE", "MATCHUP", "WL", "PLUS_MINUS"
    ]]
    games["GAME_DATE"] = pd.to_datetime(games["GAME_DATE"])

    msk_home = games["TEAM_NAME"] == team_home
    games_30_home = games[msk_home].sort_values("GAME_DATE").tail(30)
    home_plus_minus = games_30_home["PLUS_MINUS"].mean()

    msk_away = games["TEAM_NAME"] == team_away
    games_30_away = games[msk_away].sort_values("GAME_DATE").tail(30)
    away_plus_minus = games_30_away["PLUS_MINUS"].mean()

    games_diff = home_plus_minus - away_plus_minus

    diff = np.array([games_diff])
    diff_reshaped = diff.reshape(1, -1)
    predict_home_win = model.predict(diff_reshaped)[0]
    predict_winning_probability = model.predict_proba(diff_reshaped)[0][1]
    return predict_home_win, predict_winning_probability
