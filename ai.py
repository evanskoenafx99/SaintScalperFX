from engine.ai import SaintScalperBrain
from engine.vision import analyze as vision_analyze
from engine.candle_shapes import detect
from engine.pattern_detector import analyze as pattern_analyze
from engine.levels import detect_levels


def analyze_chart(filepath):

    vision = vision_analyze(filepath)

    data = detect(filepath)
    candles = data["candles"]

    pattern = pattern_analyze(candles)

    levels = detect_levels(filepath)

    brain = SaintScalperBrain()
    result = brain.analyze(candles)

    signal = result["signal"]

    if signal == "BUY":
        reason = "Bullish setup detected. AI engines confirm buying pressure."
        grade = "A"

    elif signal == "SELL":
        reason = "Bearish setup detected. AI engines confirm selling pressure."
        grade = "A"

    else:
        reason = "No high probability setup detected."
        grade = "C"


    return {
        "signal": signal,
        "trend": pattern["pattern"],
        "confidence": f"{result['confidence']}%",
        "reason": reason,

        "entry": "Wait for confirmation candle",
        "stop_loss": "Use recent support/resistance",
        "take_profit": "Minimum Risk : Reward 1:3",

        "grade": grade,
        "buy_score": result["buy_score"],
        "sell_score": result["sell_score"],
        "engines": result["engines"],

        "vision": vision,
        "candles_detected": len(candles),

        "pattern": pattern,
        "levels": levels
    }
