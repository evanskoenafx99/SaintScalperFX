def highest_high(candles, period=20):

    highs = [c["high"] for c in candles[-period:]]

    return max(highs)


def lowest_low(candles, period=20):

    lows = [c["low"] for c in candles[-period:]]

    return min(lows)


def last_close(candles):

    return candles[-1]["close"]
