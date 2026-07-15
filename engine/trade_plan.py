def generate_trade_plan(signal, pattern, momentum, levels, engines=None):

    plan = {}

    plan["signal"] = signal


    market_structure = pattern


    # Give Structure engine priority
    if engines:

        for engine in engines:

            name = engine.get("engine")


            if name == "Structure":

                if engine.get("structure") == "Bullish":
                    market_structure = "BULLISH STRUCTURE"


                elif engine.get("structure") == "Bearish":
                    market_structure = "BEARISH STRUCTURE"



    plan["market_structure"] = market_structure

    plan["momentum"] = momentum



    # Determine preparation state

    if signal == "BUY":

        if "SELLING" in momentum:

            plan["setup_state"] = "PREPARE BUY"

            plan["entry"] = (
                "Wait for bullish confirmation candle "
                "after selling pressure weakens"
            )

            plan["stop_loss"] = (
                "Below nearest strong support"
            )

            plan["take_profit"] = (
                "Next resistance zone"
            )


        else:

            plan["setup_state"] = "BUY CONFIRMED"

            plan["entry"] = (
                "Enter after bullish confirmation candle"
            )

            plan["stop_loss"] = (
                "Below nearest strong support"
            )

            plan["take_profit"] = (
                "Next resistance zone"
            )



    elif signal == "SELL":


        if "BUYING" in momentum:

            plan["setup_state"] = "PREPARE SELL"

            plan["entry"] = (
                "Wait for bearish confirmation candle "
                "after buying pressure weakens"
            )

            plan["stop_loss"] = (
                "Above nearest strong resistance"
            )

            plan["take_profit"] = (
                "Next support zone"
            )


        else:

            plan["setup_state"] = "SELL CONFIRMED"

            plan["entry"] = (
                "Enter after bearish confirmation candle"
            )

            plan["stop_loss"] = (
                "Above nearest strong resistance"
            )

            plan["take_profit"] = (
                "Next support zone"
            )



    else:

        plan["setup_state"] = "WAIT"

        plan["entry"] = "No trade"

        plan["stop_loss"] = "No trade"

        plan["take_profit"] = "No trade"



    # Setup quality score

    score = 50


    if "STRONG" in momentum:
        score += 20


    if levels.get("support"):
        score += 10


    if levels.get("resistance"):
        score += 10


    if signal != "WAIT":
        score += 10


    if score > 100:
        score = 100


    plan["setup_quality"] = score


    return plan
