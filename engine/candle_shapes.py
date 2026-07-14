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


            # Bearish candle colour
            if r > 150 and g < 120 and b < 120:
                count += 1
                bearish_pixels += 1


            # Bullish dark green candle colour
            elif g > r and g > b:
                count += 1
                bullish_pixels += 1


        if count > 2:
            active.append(x)



    # Group active columns

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

        width = end - start


        # Split large zones
        if width > 25:

            parts = max(1, width // 10)

            step = width / parts


            for i in range(parts):

                candle_start = int(start + (i * step))
                candle_end = int(start + ((i + 1) * step))


                candles.append(
                    {
                        "start": candle_start,
                        "end": candle_end,
                        "width": candle_end - candle_start
                    }
                )


        elif width >= 4:

            candles.append(
                {
                    "start": start,
                    "end": end,
                    "width": width
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
        "candles": candles[:50]
    }
