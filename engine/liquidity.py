def analyze(candles):

    if len(candles) < 30:
        return {
            "engine": "Liquidity",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    current = candles[-1]

    previous_highs = highs[-30:-1]
    previous_lows = lows[-30:-1]

    liquidity_high = max(previous_highs)
    liquidity_low = min(previous_lows)

    swept_high = current["high"] > liquidity_high
    swept_low = current["low"] < liquidity_low

    if swept_high and current["close"] < liquidity_high:
        return {
            "engine": "Liquidity",
            "signal": "SELL",
            "score": 20,
            "confidence": 90,
            "reason": "Buy-side liquidity sweep and rejection detected.",
            "liquidity": "BUY_SIDE_SWEEP",
            "level": liquidity_high
        }

    if swept_low and current["close"] > liquidity_low:
        return {
            "engine": "Liquidity",
            "signal": "BUY",
            "score": 20,
            "confidence": 90,
            "reason": "Sell-side liquidity sweep and rejection detected.",
            "liquidity": "SELL_SIDE_SWEEP",
            "level": liquidity_low
        }

    return {
        "engine": "Liquidity",
        "signal": "WAIT",
        "score": 8,
        "confidence": 40,
        "reason": "No liquidity sweep detected.",
        "liquidity": "NONE",
        "high_level": liquidity_high,
        "low_level": liquidity_low
    }
