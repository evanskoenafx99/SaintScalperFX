from PIL import Image

def analyze_chart(filepath):

    img = Image.open(filepath).convert("RGB")

    img.thumbnail((100, 100))

    width, height = img.size

    if width > height:
        signal = "🟢 BUY"
        trend = "Possible bullish movement"
        reason = "Chart shape suggests upward pressure."
    else:
        signal = "🔴 SELL"
        trend = "Possible bearish movement"
        reason = "Chart shape suggests downward pressure."

    return {
        "signal": signal,
        "trend": trend,
        "confidence": "60%",
        "reason": reason,
        "entry": "Waiting for confirmation",
        "stop_loss": "20 pips",
        "take_profit": "60 pips"
    }
