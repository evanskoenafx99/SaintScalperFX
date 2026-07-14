def analyze(candles):

    if len(candles) < 6:
        return {
            "engine": "Structure",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }


    highs = [c["high"] for c in candles[-6:]]
    lows = [c["low"] for c in candles[-6:]]


    previous_high = max(highs[:-1])
    previous_low = min(lows[:-1])

    current = candles[-1]


    bullish_bos = current["high"] > previous_high
    bearish_bos = current["low"] < previous_low


    previous_direction = None

    if highs[-2] > highs[-3] and lows[-2] > lows[-3]:
        previous_direction = "BULLISH"

    elif highs[-2] < highs[-3] and lows[-2] < lows[-3]:
        previous_direction = "BEARISH"


    choch = False


    if previous_direction == "BULLISH" and bearish_bos:
        choch = True

    if previous_direction == "BEARISH" and bullish_bos:
        choch = True



    if bullish_bos:

        return {
            "engine": "Structure",
            "signal": "BUY",
            "score": 25,
            "confidence": 95,
            "reason": "Bullish BOS detected.",
            "structure": "Bullish",
            "bos": True,
            "choch": choch
        }


    if bearish_bos:

        return {
            "engine": "Structure",
            "signal": "SELL",
            "score": 25,
            "confidence": 95,
            "reason": "Bearish BOS detected.",
            "structure": "Bearish",
            "bos": True,
            "choch": choch
        }


    return {
        "engine": "Structure",
        "signal": "WAIT",
        "score": 10,
        "confidence": 50,
        "reason": "No BOS or CHoCH detected.",
        "structure": "Sideways",
        "bos": False,
        "choch": False
    }
