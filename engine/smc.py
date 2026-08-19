from engine.structure import analyze as structure_analyze
from engine.liquidity import analyze as liquidity_analyze
from engine.fvg import analyze as fvg_analyze
from engine.orderblocks import analyze as orderblock_analyze


def analyze(candles):

    if len(candles) < 5:
        return {
            "engine": "SMC",
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

    if structure.get("signal") == "BUY":
        signal = "BUY"
        score += 20
        reasons.append("Bullish BOS")

    elif structure.get("signal") == "SELL":
        signal = "SELL"
        score += 20
        reasons.append("Bearish BOS")

    if signal != "WAIT":

        if liquidity.get("signal") == signal:
            score += 15
            reasons.append("Liquidity confirmation")

        if fvg.get("signal") == signal:
            score += 10
            reasons.append("FVG confirmation")

        if orderblock.get("signal") == signal:
            score += 15
            reasons.append("Order block confirmation")

    if structure.get("choch") and liquidity.get("signal") != "WAIT":
        signal = liquidity.get("signal")
        score = 25
        reasons.append("CHoCH reversal")
    confidence = min(score * 4, 95)


    if score < 10:
        signal = "WAIT"

    return {
        "engine": "SMC",
        "signal": signal,
        "score": score,
        "confidence": confidence,
        "reason": ", ".join(reasons) if reasons else "No SMC setup.",
        "bos": structure.get("bos", False),
        "choch": structure.get("choch", False),
        "liquidity": liquidity.get("signal") != "WAIT",
        "fvg": fvg.get("signal") != "WAIT",
        "orderblock": orderblock.get("signal") != "WAIT"
    }
