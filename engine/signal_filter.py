def validate_signal(signal, pattern, momentum, confidence_status, engines=None):

    if confidence_status == "WAIT":
        return {
            "signal": "WAIT",
            "reason": "Confidence too low."
        }


    buy_votes = 0
    sell_votes = 0

    liquidity_conflict = False


    if engines:

        for engine in engines:

            engine_signal = engine.get("signal")

            score = engine.get("score", 0)


            if engine_signal == "BUY":
                buy_votes += score


            elif engine_signal == "SELL":
                sell_votes += score


            if engine.get("engine") == "Liquidity":

                if engine_signal == "SELL":
                    liquidity_conflict = True



    # BUY validation

    if signal == "BUY":

        # Block if strong bearish momentum
        if "SELLING" in momentum:

            return {
                "signal": "WAIT",
                "reason": "BUY blocked. Strong selling momentum."
            }


        # Block liquidity conflict
        if liquidity_conflict:

            return {
                "signal": "WAIT",
                "reason": "BUY blocked. Liquidity conflict detected."
            }


        if buy_votes >= 50 and buy_votes > sell_votes:

            return {
                "signal": "BUY",
                "reason": "BUY engines aligned."
            }



    # SELL validation

    if signal == "SELL":

        if "BUYING" in momentum:

            return {
                "signal": "WAIT",
                "reason": "SELL blocked. Strong buying momentum."
            }


        if sell_votes >= 50 and sell_votes > buy_votes:

            return {
                "signal": "SELL",
                "reason": "SELL engines aligned."
            }



    return {
        "signal": "WAIT",
        "reason": "Signal conflict detected."
    }
