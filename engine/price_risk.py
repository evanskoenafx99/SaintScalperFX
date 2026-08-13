def calculate(signal, candles, bid, ask):

    print()
    print("=" * 50)
    print("PRICE RISK ENGINE")
    print("=" * 50)

    print("Signal :", signal)
    print("Bid    :", bid)
    print("Ask    :", ask)

    if not candles:
        print("No candles received.")
        print("=" * 50)
        return {
            "lot_size": 0.02,
            "stop_loss": 0,
            "take_profit": 0
        }

    if signal == "WAIT":
        print("Signal is WAIT.")
        print("=" * 50)
        return {
            "lot_size": 0.02,
            "stop_loss": 0,
            "take_profit": 0
        }

    entry = float(ask) if signal == "BUY" else float(bid)

    recent = candles[-10:]

    highs = [float(c["high"]) for c in recent]
    lows = [float(c["low"]) for c in recent]

    print()
    print("Entry :", entry)
    print("Highest:", max(highs))
    print("Lowest :", min(lows))

    if signal == "BUY":

        stop_loss = min(lows)

        risk = entry - stop_loss

        if risk <= 0:
            risk = entry * 0.002

        take_profit = entry + (risk * 3)

    else:

        stop_loss = max(highs)

        risk = stop_loss - entry

        if risk <= 0:
            risk = entry * 0.002

        take_profit = entry - (risk * 3)

    print()
    print("Calculated Risk :", risk)
    print("Stop Loss       :", stop_loss)
    print("Take Profit     :", take_profit)
    print("=" * 50)

    return {
        "lot_size": 0.02,
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2)
    }
