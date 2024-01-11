import pandas as pd
from db import Db
import logging
logging.basicConfig(level=logging.DEBUG)

db = Db()

df = pd.read_csv("./jobs/nbaTeams.csv", delimiter=";")

for index, row in df.iterrows():
    ins = {
        "name": row["name"],
        "abbr": row["abbr"],
        "description": row["description"],
        "logo_url": row["logo_url"],
        "nba_url": row["nba_url"],
        "town": row["town"],
    }
    db.insert_dict("basketball.teams", ins)
