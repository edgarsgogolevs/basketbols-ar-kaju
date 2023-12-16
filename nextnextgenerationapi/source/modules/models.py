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
MODEL_NAME_TO_ID_MAPPING = db.select_as_dict("SELECT id, path FROM basketball.prediction_models")
lg.info("Model name to id mapping loaded.")

MODEL_ID_TO_MODEL_MAPPING = {}
for model_id in MODEL_NAME_TO_ID_MAPPING:
    model_name = MODEL_NAME_TO_ID_MAPPING[model_id]
    model = MODEL_NAME_TO_MODEL_MAPPING[model_name]
    MODEL_ID_TO_MODEL_MAPPING[model_id] = model 
lg.info("All mappings created.")
