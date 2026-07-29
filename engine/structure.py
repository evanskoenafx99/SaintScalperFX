def analyze(candles):
    if len(candles) < 20:
        return {
            "engine": "Structure",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]

    current_close = closes[-1]

    swing_high = max(highs[-20:-1])
    swing_low = min(lows[-20:-1])

    hh = highs[-1] > highs[-2]
    hl = lows[-1] > lows[-2]
    lh = highs[-1] < highs[-2]
    ll = lows[-1] < lows[-2]

    bullish_bos = current_close > swing_high
    bearish_bos = current_close < swing_low

    trend = "RANGING"
    structure = "Sideways"
    signal = "WAIT"
    score = 10
    confidence = 50
    reason = "Range market."

    if bullish_bos:
        trend = "UPTREND"
        structure = "Bullish"
        signal = "BUY"
        score = 30
        confidence = 95
        reason = "Bullish Break of Structure."

    elif bearish_bos:
        trend = "DOWNTREND"
        structure = "Bearish"
        signal = "SELL"
        score = 30
        confidence = 95
        reason = "Bearish Break of Structure."

    choch = False

    if trend == "UPTREND" and lh:
        choch = True

    if trend == "DOWNTREND" and hl:
        choch = True

    return {
        "engine": "Structure",
        "signal": signal,
        "score": score,
        "confidence": confidence,
        "reason": reason,
        "structure": structure,
        "trend": trend,
        "bos": signal != "WAIT",
        "choch": choch,
        "hh": hh,
        "hl": hl,
        "lh": lh,
        "ll": ll,
        "swing_high": swing_high,
        "swing_low": swing_low,
        "current_close": current_close
    }
