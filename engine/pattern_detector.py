def analyze(candles):

    bullish = 0
    bearish = 0

    for candle in candles:

        if candle["direction"] == "BULLISH":
            bullish += 1

        elif candle["direction"] == "BEARISH":
            bearish += 1


    total = bullish + bearish


    if total == 0:
        return {
            "pattern": "NO DATA",
            "momentum": "UNKNOWN"
        }


    if bearish > bullish:

        if bearish / total > 0.65:
            pattern = "BEARISH CONTINUATION"
            momentum = "STRONG SELLING"

        else:
            pattern = "BEARISH BIAS"
            momentum = "SELL PRESSURE"


    elif bullish > bearish:

        if bullish / total > 0.65:
            pattern = "BULLISH CONTINUATION"
            momentum = "STRONG BUYING"

        else:
            pattern = "BULLISH BIAS"
            momentum = "BUY PRESSURE"


    else:

        pattern = "SIDEWAYS"
        momentum = "NEUTRAL"



    return {
        "bullish_candles": bullish,
        "bearish_candles": bearish,
        "pattern": pattern,
        "momentum": momentum
    }
