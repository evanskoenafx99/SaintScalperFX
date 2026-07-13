from PIL import Image
import numpy as np

def analyze_chart(filepath):

    img = Image.open(filepath).convert("RGB")

    img = img.resize((300, 300))

    pixels = np.array(img)

    gray = pixels.mean(axis=2)

    left_side = gray[:, :150].mean()
    right_side = gray[:, 150:].mean()

    if right_side > left_side:
        signal = "🟢 BUY"
        trend = "Possible bullish movement"
        reason = "The right side of the chart appears stronger than the left side."
    else:
        signal = "🔴 SELL"
        trend = "Possible bearish movement"
        reason = "The right side of the chart appears weaker than the left side."

    return {
        "signal": signal,
        "trend": trend,
        "confidence": "65%",
        "reason": reason,
        "entry": "Waiting for confirmation",
        "stop_loss": "20 pips",
        "take_profit": "60 pips"
    }
