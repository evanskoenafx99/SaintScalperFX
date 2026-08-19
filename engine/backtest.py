import json
import os


JOURNAL_FILE = "data/trades.json"


def group_stats(trades, key):

    stats = {}

    for trade in trades:

        value = trade.get(key, "UNKNOWN")

        if value not in stats:
            stats[value] = {
                "wins": 0,
                "losses": 0
            }


        if trade["result"] == "WIN":
            stats[value]["wins"] += 1

        else:
            stats[value]["losses"] += 1


        total = stats[value]["wins"] + stats[value]["losses"]

        stats[value]["win_rate"] = round(
            (stats[value]["wins"] / total) * 100,
            2
        )


    return stats



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


    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "signals": group_stats(closed, "signal"),
        "patterns": group_stats(closed, "pattern"),
        "momentum": group_stats(closed, "momentum")
    }
