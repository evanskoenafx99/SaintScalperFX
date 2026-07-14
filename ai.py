from engine.ai import SaintScalperBrain
from engine.vision import analyze as vision_analyze
from engine.candle_detector import extract


def analyze_chart(filepath):

    # Analyze uploaded image
    vision = vision_analyze(filepath)

    # Extract candles from screenshot
    data = extract(filepath)
    candles = data["candles"]

    # Run AI Brain
    brain = SaintScalperBrain()
    result = brain.analyze(candles)

    signal = result["signal"]

    if signal == "BUY":
        reason = "Multiple AI engines detected a bullish trading opportunity."
        grade = "A"
    elif signal == "SELL":
        reason = "Multiple AI engines detected a bearish trading opportunity."
        grade = "A"
    else:
        reason = "No high-probability setup detected."
        grade = "C"

    return {
        "signal": signal,
        "trend": "AI Multi-Engine",
        "confidence": f"{result['confidence']}%",
        "reason": reason,
        "entry": "Wait for confirmation candle",
        "stop_loss": "Below recent swing",
        "take_profit": "Minimum Risk : Reward 1:3",

        "grade": grade,
        "buy_score": result["buy_score"],
        "sell_score": result["sell_score"],
        "engines": result["engines"],

        "vision": vision,
        "candles_detected": len(candles)
    }
