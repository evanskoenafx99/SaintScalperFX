from engine.candles import highest_high, lowest_low, last_close

def analyze(candles):

    if len(candles) < 20:
        return {
            "engine": "Trend",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candle data."
        }

    high = highest_high(candles, 20)
    low = lowest_low(candles, 20)
    close = last_close(candles)

    if close > (high + low) / 2:

        return {
            "engine": "Trend",
            "signal": "BUY",
            "score": 18,
            "confidence": 90,
            "reason": "Price is trading in the upper half of the recent range.",
            "trend": "Bullish"
        }

    return {
        "engine": "Trend",
        "signal": "SELL",
        "score": 18,
        "confidence": 90,
        "reason": "Price is trading in the lower half of the recent range.",
        "trend": "Bearish"
    }
