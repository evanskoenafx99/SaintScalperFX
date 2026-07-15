def detect(candles):
    """
    Converts live MT5 candles into the same format
    expected by SaintScalperBrain.
    """

    formatted = []

    for candle in candles:

        formatted.append({
            "open": float(candle["open"]),
            "high": float(candle["high"]),
            "low": float(candle["low"]),
            "close": float(candle["close"])
        })

    return {
        "candles": formatted
    }
