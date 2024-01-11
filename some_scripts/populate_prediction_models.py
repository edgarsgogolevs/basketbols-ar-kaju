from db import Db
from models_data import data

db = Db()


if __name__=="__main__":
    for i,row in enumerate(data):
        print(f"inserting row {i+1} of {len(data)}")
        db.insert_dict("basketball.prediction_models", row)
    
