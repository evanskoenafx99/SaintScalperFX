import json
import os


JOURNAL_FILE = "data/trades.json"


def calculate_performance():

    if not os.path.exists(JOURNAL_FILE):
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0
        }


    with open(JOURNAL_FILE, "r") as file:
        trades = json.load(file)


    total = len(trades)

    wins = 0
    losses = 0


    for trade in trades:

        if trade.get("result") == "WIN":
            wins += 1

        elif trade.get("result") == "LOSS":
            losses += 1


    closed = wins + losses


    if closed > 0:
        win_rate = round((wins / closed) * 100, 2)
    else:
        win_rate = 0


    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate
    }
