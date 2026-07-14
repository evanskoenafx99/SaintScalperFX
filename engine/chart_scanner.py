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

        bullish = 0
        bearish = 0


        for x in range(chart.size[0]):

            column_activity = 0

            for y in range(chart.size[1]):

                r, g, b = pixels[x, y][:3]


                if g > r * 1.15 and g > b * 1.05:
                    bullish += 1
                    column_activity += 1


                elif r > g * 1.15 and r > b * 1.10:
                    bearish += 1
                    column_activity += 1


            if column_activity > 8:
                active_columns.append(x)



        # Group nearby columns into candle zones

        candles = []

        if active_columns:

            start = active_columns[0]
            previous = active_columns[0]


            for x in active_columns[1:]:

                if x - previous > 5:
                    candles.append(
                        {
                            "start": start,
                            "end": previous
                        }
                    )

                    start = x


                previous = x


            candles.append(
                {
                    "start": start,
                    "end": previous
                }
            )


        if bullish > bearish:
            trend = "BULLISH"

        elif bearish > bullish:
            trend = "BEARISH"

        else:
            trend = "NEUTRAL"



        return {
            "status": "SCANNED",
            "candles_detected": len(candles),
            "bullish_pixels": bullish,
            "bearish_pixels": bearish,
            "trend": trend,
            "candle_zones": candles[:10]
        }


    except Exception as e:

        return {
            "status": "ERROR",
            "message": str(e)
        }
