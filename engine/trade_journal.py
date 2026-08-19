import json
import os
from datetime import datetime


JOURNAL_FILE = "data/trades.json"


def save_trade(signal, confidence, pattern, momentum, entry, stop_loss, take_profit):

    os.makedirs("data", exist_ok=True)

    trade = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "signal": signal,
       "confidence": float(str(confidence).replace("%","")),
        "pattern": pattern,
        "momentum": momentum,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "result": "OPEN"
    }


    if os.path.exists(JOURNAL_FILE):

        with open(JOURNAL_FILE, "r") as file:
            trades = json.load(file)

    else:

        trades = []


    trades.append(trade)


    with open(JOURNAL_FILE, "w") as file:
        json.dump(trades, file, indent=4)


    return trade



def get_trades():

    if not os.path.exists(JOURNAL_FILE):
        return []

    with open(JOURNAL_FILE, "r") as file:
        return json.load(file)
