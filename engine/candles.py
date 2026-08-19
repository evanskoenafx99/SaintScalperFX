def highest_high(candles, period=20):

    highs = [c["high"] for c in candles[-period:]]

    return max(highs)


def lowest_low(candles, period=20):

    lows = [c["low"] for c in candles[-period:]]

    return min(lows)


def last_close(candles):

    return candles[-1]["close"]
def last_open(candles):
    return candles[-1]["open"]


def last_high(candles):
    return candles[-1]["high"]


def last_low(candles):
    return candles[-1]["low"]


def candle_range(candle):
    return candle["high"] - candle["low"]


def body_size(candle):
    return abs(candle["close"] - candle["open"])


def is_bullish(candle):
    return candle["close"] > candle["open"]


def is_bearish(candle):
    return candle["close"] < candle["open"]


def average_range(candles, period=20):

    recent = candles[-period:]

    total = 0.0

    for candle in recent:
        total += candle_range(candle)

    return total / len(recent)
