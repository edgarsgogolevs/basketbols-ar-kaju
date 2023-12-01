from joblib import load # type: ignore

logistic_regression = load("models/logistic_regression.joblib")
xgb = load("models/xgb.joblib")
random_forest = load("models/random_forest.joblib")
svc = load("models/svc.joblib")

MODEL_MAPPING = {
    "logistic_regression": logistic_regression,
    "xgb": xgb,
    "random_forest": random_forest,
    "svc": svc,
}
