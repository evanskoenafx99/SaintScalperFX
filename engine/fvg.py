def analyze(candles):

    if len(candles) < 3:
        return {
            "engine": "FVG",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    c1 = candles[-3]
    c2 = candles[-2]
    c3 = candles[-1]

    # Bullish Fair Value Gap
    if c3["low"] > c1["high"]:
        return {
            "engine": "FVG",
            "signal": "BUY",
            "score": 18,
            "confidence": 90,
            "reason": "Bullish Fair Value Gap detected.",
            "type": "Bullish"
        }

    # Bearish Fair Value Gap
    if c3["high"] < c1["low"]:
        return {
            "engine": "FVG",
            "signal": "SELL",
            "score": 18,
            "confidence": 90,
            "reason": "Bearish Fair Value Gap detected.",
            "type": "Bearish"
        }

    return {
        "engine": "FVG",
        "signal": "WAIT",
        "score": 8,
        "confidence": 40,
        "reason": "No Fair Value Gap detected.",
        "type": "None"
    }
