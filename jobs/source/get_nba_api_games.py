import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder  # type: ignore
from sys import argv
import logging
from typing import Union

from modules.db import Db

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger("get_nba_api_games")
db = Db()

DEFAULT_DATE_FROM = "01/01/2021"  # mm/dd/yyyy
NBA_LEAGUE_ID = "00"
STATS_COLS = ['MIN', 'FGM', 'FGA', 'FG_PCT',
       'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB',
       'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']


abbr_to_id_maaping = db.select_as_dict("SELECT abbr, id FROM basketball.teams")


def get_and_parse_games(date_from: str,
                        date_to: Union[str, None] = None) -> None:
    nba_args = dict(date_from_nullable=date_from,
                    league_id_nullable=NBA_LEAGUE_ID)
    if date_to:
        nba_args["date_to_nullable"] = date_to
    lg.info(f"Getting games from {date_from} to {date_to}")
    gamefinder = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=date_from,
        league_id_nullable=NBA_LEAGUE_ID)  #type: ignore
    games = gamefinder.get_data_frames()[0]
    # print cols
    left = len(games)
    lg.info(f"Total games found: {left}")
    for row in games.iterrows():
        print(f"{left} left.")
        left -= 1
        game = row[1]
        if " vs. " not in game["MATCHUP"]:
            continue
        team_home_abbr, team_away_abbr = game["MATCHUP"].split(" vs. ")
        team_home_id = abbr_to_id_maaping.get(team_home_abbr)
        team_away_id = abbr_to_id_maaping.get(team_away_abbr)
        if not team_home_id or not team_away_id:
            # TODO: for now warning but irl should be excpetion
            lg.warning(
                f"Could not find team id for {team_home_abbr} or {team_away_abbr}"
            )
            continue
        home_score = game["PTS"]
        away_score = home_score - game["PLUS_MINUS"]
        game_date = game["GAME_DATE"]
        home_won = game["WL"] == "W"
        # ins = {
        #     "team_home": team_home_id,
        #     "team_away": team_away_id,
        #     "game_date": game_date,
        #     "home_won": home_won,
        #     "score_home": home_score,
        #     "score_away": away_score,
        # }
        # db.insert_dict("basketball.games", ins)
        if not home_score:
            lg.info("Game did not happen yet")
            continue
        record = db.select(
            "SELECT * FROM basketball.games WHERE team_home = ? AND team_away = ? AND game_date = ?",
            (team_home_id, team_away_id, game_date))
        if not record:
            continue
        if record[0]["home_won"] is None or record[0][STATS_COLS[0]] is None:
            upd = {
                "home_won": home_won,
                "score_home": home_score,
                "score_away": away_score,
            }
            for col in STATS_COLS:
                upd[col] = game[col]
            whr = {
                "team_home": team_home_id,
                "team_away": team_away_id,
                "game_date": game_date,
            }
            db.update_dict("basketball.games", upd, whr)
        predictions = db.select(
            "SELECT * FROM basketball.game_predictions WHERE game_id = ?",
            (record[0]["id"], ))
        if not predictions:
            lg.info("No predictions for this game")
            continue
        lg.info(f"Updating predictions for game {record[0]['id']}")
        for p in predictions:
            if p["prediction_correct"] is not None:
                lg.info(
                    f"Prediction game:{p['game_id']} model:{p['model_id']} already checked"
                )
                continue
            lg.info(
                f"Checking prediction game:{p['game_id']} model:{p['model_id']}"
            )
            home_wins = p["home_wins"]
            if bool(home_wins) == bool(home_won):
                correct = True
            else:
                correct = False
            db.update_dict("basketball.game_predictions",
                           {"prediction_correct": correct}, {
                               "game_id": p["game_id"],
                               "model_id": p["model_id"]
                           })


def main(*args):
    if not args:
        lg.info(f"Using default date_from: {DEFAULT_DATE_FROM}")
        date_from = DEFAULT_DATE_FROM
    else:
        date_from = args[0]
        if len(args) > 1:
            date_to = args[1]
        else:
            date_to = None
    try:
        data = get_and_parse_games(date_from, date_to)
    except Exception:
        lg.fatal("Failed to get and parse games", exc_info=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main(*argv[1:])
