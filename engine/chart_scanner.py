from PIL import Image


def scan(filepath):

    try:
        img = Image.open(filepath)

        width, height = img.size

        chart = img.crop((
            int(width * 0.08),
            int(height * 0.20),
            int(width * 0.90),
            int(height * 0.75)
        ))

        pixels = chart.load()

        active_columns = []

        bullish_pixels = 0
        bearish_pixels = 0


        for x in range(chart.size[0]):

            activity = 0

            for y in range(chart.size[1]):

                r, g, b = pixels[x, y][:3]


                # bullish candle colour
                if g > r * 1.15 and g > b * 1.05:
                    bullish_pixels += 1
                    activity += 1


                # bearish candle colour
                elif r > g * 1.15 and r > b * 1.10:
                    bearish_pixels += 1
                    activity += 1


            if activity > 8:
                active_columns.append(x)



        # Group columns

        raw_zones = []

        if active_columns:

            start = active_columns[0]
            previous = active_columns[0]


            for x in active_columns[1:]:

                if x - previous > 5:

                    raw_zones.append(
                        (start, previous)
                    )

                    start = x


                previous = x


            raw_zones.append(
                (start, previous)
            )



        # Remove unrealistic zones

        candles = []

        for start, end in raw_zones:

            width = end - start

            # keep candle-like widths
            if 3 <= width <= 25:

                candles.append(
                    {
                        "start": start,
                        "end": end,
                        "width": width
                    }
                )



        if bullish_pixels > bearish_pixels:
            trend = "BULLISH"

        elif bearish_pixels > bullish_pixels:
            trend = "BEARISH"

        else:
            trend = "NEUTRAL"



        return {
            "status": "SCANNED",
            "candles_detected": len(candles),
            "bullish_pixels": bullish_pixels,
            "bearish_pixels": bearish_pixels,
            "trend": trend,
            "candles": candles[:20]
        }


    except Exception as e:

        return {
            "status": "ERROR",
            "message": str(e)
        }
