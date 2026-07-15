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

    buy_score = 0
    sell_score = 0
    reasons = []

    bos = structure.get("bos", False)
    choch = structure.get("choch", False)

    # Market structure
    if structure.get("signal") == "BUY":
        buy_score += 15
        reasons.append("Bullish BOS")

    if structure.get("signal") == "SELL":
        sell_score += 15
        reasons.append("Bearish BOS")

    # Liquidity
    if liquidity.get("signal") == "BUY":
        buy_score += 15
        reasons.append("Liquidity sweep for BUY")

    if liquidity.get("signal") == "SELL":
        sell_score += 15
        reasons.append("Liquidity sweep for SELL")

    # Fair Value Gap
    if fvg.get("signal") == "BUY":
        buy_score += 10
        reasons.append("Bullish FVG")

    if fvg.get("signal") == "SELL":
        sell_score += 10
        reasons.append("Bearish FVG")

    # Order Blocks
    if orderblock.get("signal") == "BUY":
        buy_score += 15
        reasons.append("Bullish order block")

    if orderblock.get("signal") == "SELL":
        sell_score += 15
        reasons.append("Bearish order block")


    if buy_score > sell_score:
        signal = "BUY"
        score = buy_score

    elif sell_score > buy_score:
        signal = "SELL"
        score = sell_score

    else:
        signal = "WAIT"
        score = 10


    confidence = min(score * 2, 95)


    return {
        "engine": "SMC",
        "signal": signal,
        "score": score,
        "confidence": confidence,
        "reason": ", ".join(reasons) if reasons else "No SMC setup.",
        "bos": bos,
        "choch": choch,
        "orderblock": orderblock.get("signal") != "WAIT",
        "liquidity": liquidity.get("signal") != "WAIT",
        "fvg": fvg.get("signal") != "WAIT"
    }
