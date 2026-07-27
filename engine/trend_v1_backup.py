from engine.candles import highest_high, lowest_low, last_close


def analyze(candles):

    if len(candles) < 20:

        return {
            "engine": "Trend",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candle data.",
            "trend": "UNKNOWN"
        }


    high = highest_high(candles, 20)

    low = lowest_low(candles, 20)

    close = last_close(candles)


    midpoint = (high + low) / 2



    if close > midpoint:

        return {

            "engine": "Trend",

            "signal": "BUY",

            "score": 18,

            "confidence": 90,

            "reason":
            "Price is above the 20 candle equilibrium.",

            "trend":
            "Bullish",

            "bias":
            "BUYING PRESSURE"

        }



    return {

        "engine": "Trend",

        "signal": "SELL",

        "score": 18,

        "confidence": 90,

        "reason":
        "Price is below the 20 candle equilibrium.",

        "trend":
        "Bearish",

        "bias":
        "SELLING PRESSURE"

    }
