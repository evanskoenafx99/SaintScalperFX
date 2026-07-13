def analyze(candles):

    if len(candles) < 6:
        return {
            "engine": "Liquidity",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    highs = [c["high"] for c in candles[-6:]]
    lows = [c["low"] for c in candles[-6:]]

    highest = max(highs)
    lowest = min(lows)

    last = candles[-1]

    buy_sweep = last["high"] >= highest
    sell_sweep = last["low"] <= lowest

    if buy_sweep:
        return {
            "engine": "Liquidity",
            "signal": "SELL",
            "score": 18,
            "confidence": 90,
            "reason": "Buy-side liquidity sweep detected."
        }

    if sell_sweep:
        return {
            "engine": "Liquidity",
            "signal": "BUY",
            "score": 18,
            "confidence": 90,
            "reason": "Sell-side liquidity sweep detected."
        }

    return {
        "engine": "Liquidity",
        "signal": "WAIT",
        "score": 8,
        "confidence": 40,
        "reason": "No liquidity sweep detected."
    }
