import logging
from typing import Union

from modules.db import Db

db = Db()
lg = logging.getLogger("modules.teams")

def get_team_name_by_id(team_id: int) -> Union[str, None]:
    data = db.select("SELECT name FROM basketball.teams WHERE id=?", (team_id,))
    if not data:
        return None
    return data[0]["name"]
