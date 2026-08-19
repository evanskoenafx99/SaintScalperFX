from PIL import Image


def extract(filepath):
    """
    Temporary candle extractor.
    This will later detect real candles from the chart image.
    """

    img = Image.open(filepath)

    width, height = img.size

    candles = []

    # Temporary dummy candles
    for i in range(30):

        candles.append({
            "open": 1.1000 + (i * 0.0001),
            "high": 1.1005 + (i * 0.0001),
            "low": 1.0995 + (i * 0.0001),
            "close": 1.1002 + (i * 0.0001)
        })

    return {
        "image_width": width,
        "image_height": height,
        "candles": candles
    }
