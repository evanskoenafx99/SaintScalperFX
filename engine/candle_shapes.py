from PIL import Image


def detect(filepath):

    img = Image.open(filepath).convert("RGB")

    width, height = img.size

    chart = img.crop((
        int(width * 0.08),
        int(height * 0.20),
        int(width * 0.90),
        int(height * 0.75)
    ))

    pixels = chart.load()

    active = []

    bullish_pixels = 0
    bearish_pixels = 0


    for x in range(chart.size[0]):

        count = 0

        for y in range(chart.size[1]):

            r, g, b = pixels[x, y]

            if r > 150 and g < 120 and b < 120:
                count += 1
                bearish_pixels += 1

            elif g > r and g > b:
                count += 1
                bullish_pixels += 1

        if count > 2:
            active.append(x)


    zones = []

    if active:

        start = active[0]
        previous = active[0]

        for x in active[1:]:

            if x - previous > 6:
                zones.append((start, previous))
                start = x

            previous = x

        zones.append((start, previous))


    candles = []


    for start, end in zones:

        width = end - start

        parts = 1

        if width > 25:
            parts = width // 10


        for i in range(parts):

            candle_start = int(start + (i * width / parts))
            candle_end = int(start + ((i + 1) * width / parts))


            if candle_end - candle_start >= 4:

                red = 0
                green = 0


                for cx in range(candle_start, candle_end):

                    for cy in range(chart.size[1]):

                        r, g, b = pixels[cx, cy]


                        if r > 150 and g < 120 and b < 120:
                            red += 1

                        elif g > r and g > b:
                            green += 1


                if red > green:
                    direction = "BEARISH"

                elif green > red:
                    direction = "BULLISH"

                else:
                    direction = "UNKNOWN"


                if candle_end - candle_start >= 15:
                    strength = "STRONG"

                else:
                    strength = "NORMAL"


                # Temporary OHLC conversion layer
                index = len(candles) + 1

                if direction == "BULLISH":

                    candle_open = 100 + index
                    candle_close = candle_open + 1
                    candle_high = candle_close + 0.5
                    candle_low = candle_open - 0.5

                elif direction == "BEARISH":

                    candle_open = 100 + index
                    candle_close = candle_open - 1
                    candle_high = candle_open + 0.5
                    candle_low = candle_close - 0.5

                else:

                    candle_open = 100 + index
                    candle_close = candle_open
                    candle_high = candle_open + 0.2
                    candle_low = candle_open - 0.2


                candles.append({

                    "open": candle_open,
                    "high": candle_high,
                    "low": candle_low,
                    "close": candle_close,
                    "volume": 100,

                    "start": candle_start,
                    "end": candle_end,

                    "direction": direction,
                    "strength": strength

                })


    if bullish_pixels > bearish_pixels:

        bias = "BULLISH"

    elif bearish_pixels > bullish_pixels:

        bias = "BEARISH"

    else:

        bias = "NEUTRAL"


    return {

        "candles_found": len(candles),
        "bias": bias,

        "bullish_pixels": bullish_pixels,
        "bearish_pixels": bearish_pixels,

        "candles": candles[:50]

    }
