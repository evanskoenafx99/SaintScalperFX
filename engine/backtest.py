import json
import os


def calculate_backtest():

    file = "data/trades.json"

    if not os.path.exists(file):
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0
        }


    with open(file, "r") as f:
        trades = json.load(f)


    wins = 0
    losses = 0


    for trade in trades:

        if trade["result"] == "WIN":
            wins += 1

        elif trade["result"] == "LOSS":
            losses += 1


    total = wins + losses


    win_rate = 0

    if total > 0:
        win_rate = round((wins / total) * 100, 2)


    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate
    }
