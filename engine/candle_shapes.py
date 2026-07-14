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


            # Bearish MT5 candle
            if r > 150 and g < 120 and b < 120:
                count += 1
                bearish_pixels += 1


            # Bullish MT5 candle (dark green)
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

                zones.append(
                    (start, previous)
                )

                start = x


            previous = x


        zones.append(
            (start, previous)
        )



    candles = []


    for start, end in zones:

        candle_width = end - start


        if 1 <= candle_width <= 40:

            candles.append(
                {
                    "start": start,
                    "end": end,
                    "width": candle_width
                }
            )



    if bullish_pixels > bearish_pixels:
        bias = "BULLISH"

    elif bearish_pixels > bullish_pixels:
        bias = "BEARISH"

    else:
        bias = "NEUTRAL"



    return {
        "candles_found": len(candles),
        "bullish_pixels": bullish_pixels,
        "bearish_pixels": bearish_pixels,
        "bias": bias,
        "candles": candles[:30]
    }
