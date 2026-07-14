import json
import os


JOURNAL_FILE = "data/trades.json"


def update_trade(index, result):

    if not os.path.exists(JOURNAL_FILE):
        return False


    with open(JOURNAL_FILE, "r") as file:
        trades = json.load(file)


    if index < 0 or index >= len(trades):
        return False


    trades[index]["result"] = result.upper()


    with open(JOURNAL_FILE, "w") as file:
        json.dump(trades, file, indent=4)


    return True
