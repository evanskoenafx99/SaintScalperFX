def validate_signal(signal, pattern, momentum, confidence_status):

    if confidence_status == "WAIT":
        return {
            "signal": "WAIT",
            "reason": "Confidence too low."
        }


    if signal == "BUY":

        if "BULLISH" in pattern and "BUYING" in momentum:
            return {
                "signal": "BUY",
                "reason": "Bullish pattern and momentum confirmed."
            }


    if signal == "SELL":

        if "BEARISH" in pattern and "SELLING" in momentum:
            return {
                "signal": "SELL",
                "reason": "Bearish pattern and momentum confirmed."
            }


    return {
        "signal": "WAIT",
        "reason": "Signal conflict detected."
    }
