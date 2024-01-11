import logging

from joblib import load  # type: ignore
from modules.db import Db

lg = logging.getLogger("modules.models")
db = Db()

lg.info("Loading models..")
logistic_regression = load("models/logistic_regression.joblib")
xgb = load("models/xgb.joblib")
random_forest = load("models/random_forest.joblib")
svc = load("models/svc.joblib")
lg.info("Models loaded.")

MODEL_NAME_TO_MODEL_MAPPING = {
    "logistic_regression": logistic_regression,
    "xgb": xgb,
    "random_forest": random_forest,
    "svc": svc,
}

lg.info("Loading model name to id mapping...")
MODEL_NAME_TO_ID_MAPPING = db.select_as_dict(
    "SELECT id, path FROM basketball.prediction_models")
lg.info("Model name to id mapping loaded.")

MODEL_ID_TO_MODEL_MAPPING = {}
for model_id in MODEL_NAME_TO_ID_MAPPING:
    model_name = MODEL_NAME_TO_ID_MAPPING[model_id]
    model = MODEL_NAME_TO_MODEL_MAPPING[model_name]
    MODEL_ID_TO_MODEL_MAPPING[model_id] = model
lg.info("All mappings created.")

Q = """
SET ROWCOUNT 1000;
SELECT gp.*, g.* FROM
basketball.game_predictions gp INNER JOIN basketball.games g
ON gp.game_id=g.id
WHERE gp.model_id=? AND gp.prediction_correct IS NOT NULL
ORDER BY g.game_date DESC;
"""

GAME_STATS_COLS = ['MIN', 'FGM', 'FGA', 'FG_PCT',
       'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB',
       'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']

def calculate_model_stats(model_id: int) -> dict:
    ret = {}
    last_preds = db.select(Q, (model_id, ))
    last_ten = last_preds[:10]
    all_time_acc = calculate_accuracy(last_preds)
    last_ten_acc = calculate_accuracy(last_ten)
    ret["last_ten_accuracy"] = last_ten_acc
    ret["all_time_accuracy"] = all_time_acc
    return ret


def calculate_accuracy(last_preds: list[dict]) -> float:
    correct_preds = 0
    for p in last_preds:
        if p["prediction_correct"]:
            correct_preds += 1
    return correct_preds / len(last_preds)


def create_history(model_id: int) -> list[dict]:
    last_preds = db.select(Q, (model_id, ))
    history: list[dict] = []
    for rec in reversed(last_preds):
        game = {
            "team_home_id": rec["team_home"],
            "team_away_id": rec["team_away"],
            "home_won": rec["home_won"],
            "game_date": rec["game_date"],
            "score_home": rec["score_home"],
            "score_away": rec["score_away"],
        }
        for col in GAME_STATS_COLS:
            if col in rec:
                game[col] = rec[col]
        pred = {
            "game": game,
            "game_id": rec["game_id"],
            "model_id": rec["model_id"],
            "home_wins": rec["home_wins"],
            "home_winning_proba": rec["home_winning_proba"],
            "prediction_correct": rec["prediction_correct"],
            "updated_at": rec["updated_at"]
        }
        history.append(pred)
    return history
