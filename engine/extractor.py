from engine.vision import read_chart


def extract_candles(filepath):

    chart = read_chart(filepath)

    width = chart["width"]
    height = chart["height"]

    candles = []

    # Temporary candles
    # These will later come from real chart recognition
    for i in range(100):

        candles.append(
            {
                "open": 1.1000,
                "high": 1.1010,
                "low": 1.0990,
                "close": 1.1005
            }
        )

    return candles
