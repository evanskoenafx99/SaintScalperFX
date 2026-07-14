import json
import os


JOURNAL_FILE = "data/trades.json"


def calculate_backtest():

    if not os.path.exists(JOURNAL_FILE):
        return {}


    with open(JOURNAL_FILE, "r") as file:
        trades = json.load(file)


    closed = [
        t for t in trades
        if t.get("result") in ["WIN", "LOSS"]
    ]


    wins = sum(1 for t in closed if t["result"] == "WIN")
    losses = sum(1 for t in closed if t["result"] == "LOSS")


    total = len(closed)

    win_rate = 0

    if total:
        win_rate = round((wins / total) * 100, 2)


    signal_stats = {}

    for trade in closed:

        signal = trade.get("signal")

        if signal not in signal_stats:
            signal_stats[signal] = {
                "wins": 0,
                "losses": 0
            }


        if trade["result"] == "WIN":
            signal_stats[signal]["wins"] += 1

        else:
            signal_stats[signal]["losses"] += 1


    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "signals": signal_stats
    }
