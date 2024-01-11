import requests as r # type: ignore
from time import sleep

from db import Db

db = Db()

abbr_to_id_maaping = db.select_as_dict("SELECT abbr, id FROM basketball.teams")
START_DATE = "2023-12-15"
URL = "https://www.balldontlie.io/api/v1/games?seasons[]=2023&page={current_page}&per_page=10&start_date={start_date}"


def get_standigs():
    r_data = {"current_page": 1, "start_date": START_DATE}
    next_page = 1
    cur_sleep = 3
    while next_page:
        print(f"Getting page {next_page}...")
        r_data["current_page"] = next_page
        url = URL.format(**r_data)
        resp = r.get(url)
        if resp.status_code == 429:
            print("Sleeping...")
            sleep(cur_sleep)
            cur_sleep = int(cur_sleep * 1.2)
            continue
        cur_sleep = 3
        resp_json = resp.json()
        data = resp_json["data"]
        meta = resp_json["meta"]
        next_page = meta["next_page"]
        for row in data:
            ins = {
                "game_date": row["date"].split("T")[0],
                "team_home": abbr_to_id_maaping[row["home_team"]["abbreviation"]],
                "team_away": abbr_to_id_maaping[row["visitor_team"]["abbreviation"]],
            }
            try:
                db.insert_dict("basketball.games", ins)
            except Exception as e:
                print(e)
                print("Error inserting:")
                print(ins)
                print("Continuing...")


def main():
    get_standigs()


if __name__ == "__main__":
    main()
