from engine.candles import (
    highest_high,
    lowest_low,
    last_close,
    average_range
)

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

    price_range = high - low

    distance = abs(close - midpoint)

    strength = "WEAK"

    if distance > average_range(candles, 20):
        strength = "STRONG"
    elif distance > average_range(candles, 20) / 2:
        strength = "MODERATE"

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
            "BUYING PRESSURE",
           "equilibrium": midpoint,

           "close": close,

           "zone": "PREMIUM",

           "strength": strength,

          "distance": distance,
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
        "SELLING PRESSURE",
       "equilibrium": midpoint,

       "close": close,

       "zone": "DISCOUNT",

       "strength": strength,

       "distance": distance,
    }
