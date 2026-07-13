def analyze(candles):

    if len(candles) < 4:
        return {
            "engine": "Structure",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }

    h1 = candles[-4]["high"]
    h2 = candles[-3]["high"]
    h3 = candles[-2]["high"]
    h4 = candles[-1]["high"]

    l1 = candles[-4]["low"]
    l2 = candles[-3]["low"]
    l3 = candles[-2]["low"]
    l4 = candles[-1]["low"]

    bullish = h4 > h3 and l4 > l3
    bearish = h4 < h3 and l4 < l3

    if bullish:
        return {
            "engine": "Structure",
            "signal": "BUY",
            "score": 20,
            "confidence": 95,
            "reason": "Higher High and Higher Low detected.",
            "structure": "Bullish",
            "bos": True,
            "choch": False
        }

    if bearish:
        return {
            "engine": "Structure",
            "signal": "SELL",
            "score": 20,
            "confidence": 95,
            "reason": "Lower High and Lower Low detected.",
            "structure": "Bearish",
            "bos": True,
            "choch": False
        }

    return {
        "engine": "Structure",
        "signal": "WAIT",
        "score": 10,
        "confidence": 50,
        "reason": "No clear market structure.",
        "structure": "Sideways",
        "bos": False,
        "choch": False
    }
