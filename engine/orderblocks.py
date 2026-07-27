def analyze(candles):

    if len(candles) < 5:
        return {
            "engine": "Order Blocks",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    last = candles[-1]
    previous = candles[-2]

    # Bullish Order Block
    if previous["close"] < previous["open"] and last["close"] > previous["high"]:
        return {
            "engine": "Order Blocks",
            "signal": "BUY",
            "score": 19,
            "confidence": 92,
            "reason": "Bullish Order Block confirmed.",
            "type": "Bullish",
            "order_block": True
        }

    # Bearish Order Block
    if previous["close"] > previous["open"] and last["close"] < previous["low"]:
        return {
            "engine": "Order Blocks",
            "signal": "SELL",
            "score": 19,
            "confidence": 92,
            "reason": "Bearish Order Block confirmed.",
           "type": "Bearish",
           "order_block": True
        }

    return {
        "engine": "Order Blocks",
        "signal": "WAIT",
        "score": 8,
        "confidence": 40,
        "reason": "No Order Block detected.",
       "type": "None",
       "order_block": False
    }
