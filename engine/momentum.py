def analyze(candles):

    if len(candles) < 3:
        return {
            "engine": "Momentum",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "momentum": "NEUTRAL",
            "reason": "Not enough candles."
        }

    bullish = 0
    bearish = 0

    for candle in candles[-3:]:

        if candle["close"] > candle["open"]:
            bullish += 1

        elif candle["close"] < candle["open"]:
            bearish += 1

    if bullish >= 3:
        return {
            "engine": "Momentum",
            "signal": "BUY",
            "score": 10,
            "confidence": 90,
            "momentum": "STRONG BUYING",
            "reason": "Bullish momentum increasing."
        }

    elif bearish >= 3:
        return {
            "engine": "Momentum",
            "signal": "SELL",
            "score": 10,
            "confidence": 90,
            "momentum": "STRONG SELLING",
            "reason": "Bearish momentum increasing."
        }

    return {
        "engine": "Momentum",
        "signal": "WAIT",
        "score": 5,
        "confidence": 50,
        "momentum": "NEUTRAL",
        "reason": "Momentum is mixed."
    }
