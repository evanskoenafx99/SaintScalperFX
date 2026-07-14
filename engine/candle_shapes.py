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


    for x in range(chart.size[0]):

        count = 0

        for y in range(chart.size[1]):

            r, g, b = pixels[x, y]


            # MT5 red candle detection
            if r > 150 and g < 120 and b < 120:
                count += 1


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

        width = end - start


        if 1 <= width <= 40:

            candles.append(
                {
                    "start": start,
                    "end": end,
                    "width": width
                }
            )


    return {
        "candles_found": len(candles),
        "candles": candles[:30]
    }
