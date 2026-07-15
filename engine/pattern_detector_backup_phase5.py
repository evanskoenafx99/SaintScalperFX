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


    bullish_ratio = bullish / total
    bearish_ratio = bearish / total


    # Candle momentum detection

    if bullish_ratio > 0.65:

        pattern = "BULLISH CONTINUATION"
        momentum = "STRONG BUYING"


    elif bearish_ratio > 0.65:

        pattern = "BEARISH CONTINUATION"
        momentum = "STRONG SELLING"


    elif bullish > bearish:

        pattern = "BULLISH BIAS"
        momentum = "BUY PRESSURE"


    elif bearish > bullish:

        pattern = "BEARISH BIAS"
        momentum = "SELL PRESSURE"


    else:

        pattern = "SIDEWAYS"
        momentum = "NEUTRAL"



    return {

        "bullish_candles": bullish,

        "bearish_candles": bearish,

        "bullish_ratio": round(bullish_ratio, 2),

        "bearish_ratio": round(bearish_ratio, 2),

        "pattern": pattern,

        "momentum": momentum

    }
