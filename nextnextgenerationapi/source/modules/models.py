import logging

from joblib import load  # type: ignore
from modules.db import Db
from schemas.GamePredictionSchema import ModelStatsSchema

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


def calculate_model_stats(model_id: int) -> ModelStatsSchema:
    model_data = db.select(
        "select * from basketball.prediction_models where id=?",
        (model_id, ))[0]
    ret = {"nominal_accuracy": model_data["nominal_precision"]}
    q = """
    SET ROWCOUNT 1000;
    SELECT gp.*, g.* FROM
    basketball.game_predictions gp INNER JOIN basketball.games g
    ON gp.game_id=g.id
    WHERE gp.model_id=? AND gp.prediction_correct IS NOT NULL
    ORDER BY g.game_date DESC;
    """
    last_preds = db.select(q, (model_id, ))
    last_ten = last_preds[:10]
    all_time_acc = calculate_accuracy(last_preds)
    last_ten_acc = calculate_accuracy(last_ten)
    ret["last_ten_accuracy"] = last_ten_acc
    ret["all_time_accuracy"] = all_time_acc
    ret["prediction_history"] = create_history(last_preds)
    return ret


def calculate_accuracy(last_preds: list[dict]) -> float:
    correct_preds = 0
    for p in last_preds:
        if p["prediction_correct"]:
            correct_preds += 1
    return correct_preds / len(last_preds)


def create_history(last_preds: list[dict]) -> list[dict]:
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
