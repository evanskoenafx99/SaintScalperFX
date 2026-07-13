from engine.ai import SaintScalperBrain


def analyze_chart(filepath):

    # Temporary candle data
    # Later this will come from MT5 or chart extraction
    candles = [
        {
            "open": 1,
            "high": 2,
            "low": 0.5,
            "close": 1.5
        }
        for _ in range(20)
    ]

    brain = SaintScalperBrain()

    result = brain.analyze(candles)

    signal = result["signal"]

    if signal == "BUY":
        reason = "AI detected bullish conditions across multiple engines."

    elif signal == "SELL":
        reason = "AI detected bearish conditions across multiple engines."

    else:
        reason = "AI did not find a strong setup."

    return {
        "signal": signal,
        "trend": "AI Multi-Engine",
        "confidence": f'{result["confidence"]}%',
        "reason": reason,
        "entry": "Waiting for market confirmation",
        "stop_loss": "20 pips",
        "take_profit": "60 pips"
    }
