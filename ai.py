from engine.ai import SaintScalperBrain
from engine.vision import analyze as vision_analyze
from engine.candle_shapes import detect
from engine.pattern_detector import analyze as pattern_analyze
from engine.levels import detect_levels
from engine.trade_plan import generate_trade_plan
from engine.confidence_filter import evaluate_confidence


def analyze_chart(filepath):

    vision = vision_analyze(filepath)

    data = detect(filepath)
    candles = data["candles"]

    pattern = pattern_analyze(candles)

    levels = detect_levels(filepath)

    brain = SaintScalperBrain()
    result = brain.analyze(candles)

    signal = result["signal"]

    confidence_check = evaluate_confidence(result["confidence"])

    grade = confidence_check["grade"]


    if signal == "BUY":

        reason = "Bullish setup detected by AI engines."


    elif signal == "SELL":

        reason = "Bearish setup detected by AI engines."


    else:

        reason = "No high probability setup detected."


    trade_plan = generate_trade_plan(
        signal,
        pattern["pattern"],
        pattern["momentum"],
        levels
    )


    return {

        "signal": signal,

        "trend": pattern["pattern"],

        "confidence": f"{result['confidence']}%",

        "confidence_status": confidence_check["status"],

        "confidence_message": confidence_check["message"],

        "reason": reason,

        "entry": trade_plan["entry"],

        "stop_loss": trade_plan["stop_loss"],

        "take_profit": trade_plan["take_profit"],

        "grade": grade,

        "buy_score": result["buy_score"],

        "sell_score": result["sell_score"],

        "engines": result["engines"],

        "vision": vision,

        "candles_detected": len(candles),

        "pattern": pattern,

        "levels": levels,

        "trade_plan": trade_plan
    }
