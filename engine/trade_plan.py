def generate_trade_plan(signal, pattern, momentum, levels):

    plan = {}

    plan["signal"] = signal

    plan["market_structure"] = pattern

    plan["momentum"] = momentum


    if signal == "BUY":

        plan["entry"] = "Wait for bullish confirmation candle"

        plan["stop_loss"] = "Below nearest strong support"

        plan["take_profit"] = "Next resistance zone"


    elif signal == "SELL":

        plan["entry"] = "Wait for bearish confirmation candle"

        plan["stop_loss"] = "Above nearest strong resistance"

        plan["take_profit"] = "Next support zone"


    else:

        plan["entry"] = "No trade"

        plan["stop_loss"] = "No trade"

        plan["take_profit"] = "No trade"



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
