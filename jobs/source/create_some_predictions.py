import logging
import requests as r
import time
import datetime
import sys

from modules.db import Db

API_URL = "http://localhost:8069"

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger("get_nba_api_games")

db = Db()


def get_models():
    lg.info("Getting models..")
    resp = r.get(f"{API_URL}/models/all")
    if resp.status_code != 200:
        raise Exception("Could not get models")
    return resp.json()


def get_games(rowcount: int, upcoming=False) -> list[dict]:
    if not upcoming:
        lg.info(f"Getting {'upcoming' if upcoming else 'recent'} games..")
        return db.select(
            f"SET ROWCOUNT {rowcount}; select * from basketball.games where home_won is not null order by game_date desc"
        )
    to_date = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    lg.info(f"Getting upcoming games from {to_date}")
    return db.select(
        f"SET ROWCOUNT {rowcount}; select * from basketball.games where home_won is null AND game_date > ? order by game_date asc",
        (to_date, )
    )


def check_if_exists(db_data: list[dict], model_data: dict):
    if not db_data:
        return False
    for d in db_data:
        if d["model_id"] == model_data["id"]:
            return True
    return False


def check_prediction_correct(game: dict, prediction: dict):
    lg.info(f"Checking if prediction is correct for {game['id']}")
    home_won = game["home_won"]
    predicted = prediction["home_wins"]
    if bool(home_won) == bool(predicted):
        correct = True
    else:
        correct = False
    if not db.update_dict("basketball.game_predictions",
                   {"prediction_correct": correct}, {
                       "model_id": prediction["model_id"],
                       "game_id": prediction["game_id"]
                          }):
        raise Exception("Could not update prediction")


def make_prediction(game: dict, models: list[dict]):
    exists = db.select(
        "select * from basketball.game_predictions where game_id = ? and prediction_correct is not null",
        (game["id"], ))
    for m in models:
        time.sleep(.6)
        if check_if_exists(exists, m):
            lg.info(
                f"Prediction for {game['id']} and model {m['id']} already exists"
            )
            continue
        lg.info(f"Making prediction for {game['id']} and model {m['id']}")
        try:
            resp = r.get(
                f"{API_URL}/predictions/predict_game/{game['id']}/{m['id']}")
            if resp.status_code not in (200, 201):
                lg.error(
                    f"Could not make prediction for {game['id']} and model {m['id']}"
                )
                continue
            lg.info(
                f"Prediction for {game['id']} and model {m['id']} made successfully"
            )
            # check_prediction_correct(game, resp.json())
        except Exception:
            lg.error(
                f"Could not make prediction for {game['id']} and model {m['id']}",
                exc_info=True)
            continue


def run(upcoming=False):
    models = get_models()
    games = get_games(50, upcoming)
    left = len(games)
    lg.info(f"Making predictions for {left} games")
    for game in games:
        lg.info(f"{left} games left")
        left -= 1
        make_prediction(game, models)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "upcoming":
        upcoming = True
    else:
        upcoming = False
    run(upcoming)
