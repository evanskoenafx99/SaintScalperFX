def calculate(signal, candles, bid, ask):

    if not candles or signal == "WAIT":
        return {
            "stop_loss": 0,
            "take_profit": 0
        }

    entry = ask if signal == "BUY" else bid

    recent = candles[-10:]

    highs = [c["high"] for c in recent]
    lows = [c["low"] for c in recent]

    if signal == "BUY":

        stop_loss = min(lows)

        risk = entry - stop_loss

        take_profit = entry + (risk * 3)

    elif signal == "SELL":

        stop_loss = max(highs)

        risk = stop_loss - entry

        take_profit = entry - (risk * 3)

    else:
        stop_loss = 0
        take_profit = 0


    return {
        "stop_loss": round(stop_loss, 5),
        "take_profit": round(take_profit, 5)
    }
