from engine.structure import analyze as structure_analyze
from engine.liquidity import analyze as liquidity_analyze
from engine.fvg import analyze as fvg_analyze
from engine.orderblocks import analyze as orderblock_analyze


def analyze(candles):

    if len(candles) < 5:
        return {
            "engine": "ICT",
            "signal": "WAIT",
            "score": 0,
            "confidence": 0,
            "reason": "Not enough candles."
        }


    structure = structure_analyze(candles)
    liquidity = liquidity_analyze(candles)
    fvg = fvg_analyze(candles)
    orderblock = orderblock_analyze(candles)


    score = 0
    signal = "WAIT"
    reasons = []


    # Market structure bias
    if structure.get("signal") == "BUY":

        signal = "BUY"
        score += 20
        reasons.append("Bullish BOS")


    elif structure.get("signal") == "SELL":

        signal = "SELL"
        score += 20
        reasons.append("Bearish BOS")


    # If no BOS, use imbalance bias
    elif fvg.get("signal") == "BUY":

        signal = "BUY"
        score += 10
        reasons.append("Bullish FVG")


    elif fvg.get("signal") == "SELL":

        signal = "SELL"
        score += 10
        reasons.append("Bearish FVG")


    # Liquidity confirmation

    if liquidity.get("signal") == signal:

        score += 15
        reasons.append("Liquidity confirmation")


    # Fair Value Gap confirmation

    if fvg.get("signal") == signal:

        score += 10
        reasons.append("FVG confirmation")


    # Order block confirmation

    if orderblock.get("signal") == signal:

        score += 10
        reasons.append("Order block confirmation")


    # CHoCH reversal

    if structure.get("choch"):

        if liquidity.get("signal") != "WAIT":

            signal = liquidity.get("signal")
            score = 25
            reasons.append("CHoCH reversal")


    confidence = min(score * 3, 95)


    if score < 10:

        signal = "WAIT"



    return {

        "engine": "ICT",

        "signal": signal,

        "score": score,

        "confidence": confidence,

        "reason": ", ".join(reasons)
        if reasons else "No ICT setup.",


        "bos": structure.get("bos", False),

        "choch": structure.get("choch", False),


        "liquidity": liquidity.get("signal") != "WAIT",

        "fvg": fvg.get("signal") != "WAIT",

        "orderblock": orderblock.get("signal") != "WAIT",


        "structure_signal": structure.get("signal"),

        "liquidity_signal": liquidity.get("signal"),

        "fvg_signal": fvg.get("signal"),

        "orderblock_signal": orderblock.get("signal")

    }
