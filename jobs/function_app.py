import azure.functions as func
import datetime
import json
import logging

from source.get_nba_api_games import get_and_parse_games

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 */5 * * *",
                   arg_name="myTimer",
                   run_on_startup=True,
                   use_monitor=False)
def getNbaData(myTimer: func.TimerRequest) -> None:
    date_from = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%m/%d/%Y")
    date_to = datetime.datetime.now().strftime("%m/%d/%Y")
    logging.info(f"Updating games data from {date_from} to {date_to}")
    get_and_parse_games(date_from, date_to)
