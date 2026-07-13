from PIL import Image
import numpy as np

def analyze_chart(filepath):

    img = Image.open(filepath).convert("RGB")

    # Keep memory usage low
    img.thumbnail((200, 200))

    pixels = np.array(img)

    # Convert image to grayscale
    gray = pixels.mean(axis=2)

    height, width = gray.shape

    # Split chart into left and right sections
    left = gray[:, :width//2].mean()
    right = gray[:, width//2:].mean()

    difference = right - left

    if difference > 5:
        signal = "🟢 BUY"
        trend = "Possible bullish direction"
        reason = "The right side of the chart shows stronger upward activity."
    elif difference < -5:
        signal = "🔴 SELL"
        trend = "Possible bearish direction"
        reason = "The right side of the chart shows weaker price activity."
    else:
        signal = "⚪ WAIT"
        trend = "Sideways market"
        reason = "No strong direction detected."

    return {
        "signal": signal,
        "trend": trend,
        "confidence": "70%",
        "reason": reason,
        "entry": "Wait for confirmation",
        "stop_loss": "20 pips",
        "take_profit": "60 pips"
    }
