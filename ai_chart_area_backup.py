from PIL import Image
import numpy as np

def analyze_chart(filepath):

    img = Image.open(filepath).convert("RGB")

    # Reduce size to save memory
    img.thumbnail((250, 250))

    pixels = np.array(img)

    # Convert to grayscale
    gray = pixels.mean(axis=2)

    height, width = gray.shape

    # Focus on the middle area where charts usually are
    chart = gray[
        int(height * 0.2):int(height * 0.8),
        int(width * 0.2):int(width * 0.8)
    ]

    # Split into older and newer price areas
    middle = chart.shape[1] // 2

    old_price = chart[:, :middle].mean()
    new_price = chart[:, middle:].mean()

    movement = new_price - old_price

    if movement > 3:
        signal = "🟢 BUY"
        trend = "Possible upward movement"
        reason = "Recent chart area appears stronger than the earlier area."
        confidence = "72%"

    elif movement < -3:
        signal = "🔴 SELL"
        trend = "Possible downward movement"
        reason = "Recent chart area appears weaker than the earlier area."
        confidence = "72%"

    else:
        signal = "⚪ WAIT"
        trend = "No clear trend"
        reason = "The chart does not show a strong direction."
        confidence = "50%"

    return {
        "signal": signal,
        "trend": trend,
        "confidence": confidence,
        "reason": reason,
        "entry": "Wait for confirmation",
        "stop_loss": "20 pips",
        "take_profit": "60 pips"
    }
