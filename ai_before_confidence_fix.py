from engine.confidence_filter import evaluate_confidence
from engine.trade_journal import save_trade
from engine.ai import SaintScalperBrain
from engine.vision import analyze as vision_analyze
from engine.candle_shapes import detect
from engine.pattern_detector import analyze as pattern_analyze
from engine.levels import detect_levels
from engine.trade_plan import generate_trade_plan


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

    if pattern["pattern"] == "BEARISH CONTINUATION" and pattern["momentum"] == "STRONG SELLING":

        signal = "SELL"
        reason = "Bearish continuation confirmed by candle pattern and selling momentum."


    elif pattern["pattern"] == "BULLISH CONTINUATION" and pattern["momentum"] == "STRONG BUYING":

        signal = "BUY"
        reason = "Bullish continuation confirmed by candle pattern and buying momentum."


    elif signal == "BUY":

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

    save_trade(
        signal,
        result["confidence"],
        pattern["pattern"],
        pattern["momentum"],
        "Wait for confirmation candle",
        "Use recent support/resistance",
        "Minimum Risk : Reward 1:3"
    )

    return {

        "signal": signal,

        "trend": pattern["pattern"],

        "confidence": f"{result['confidence']}%",

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

        "candle_count": len(candles),

        "candle_bias": pattern["pattern"],

        "bullish_candles": pattern["bullish_candles"],

        "bearish_candles": pattern["bearish_candles"],


        "pattern": pattern["pattern"],

        "momentum": pattern["momentum"],

        "levels": levels,

        "trade_plan": trade_plan
    "confidence_status": confidence_check["status"],
"confidence_message": confidence_check["message"],
    }
