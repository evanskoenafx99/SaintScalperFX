from PIL import Image
from engine.candle_shapes import detect


def detect_levels(image_path):

    img = Image.open(image_path).convert("RGB")

    width, height = img.size

    candles = detect(image_path)["candles"]

    supports = []
    resistances = []


    for candle in candles:

        x = int((candle["start"] + candle["end"]) / 2)

        candle_pixels = []


        for y in range(int(height * 0.15), int(height * 0.75)):

            r, g, b = img.getpixel((x, y))

            if r > 100 or g > 100 or b > 100:
                candle_pixels.append(y)


        if candle_pixels:

            high = min(candle_pixels)
            low = max(candle_pixels)

            resistances.append(high)
            supports.append(low)



    def build_zones(values):

        zones = []

        if not values:
            return zones


        values.sort()

        start = values[0]
        end = values[0]
        touches = 1


        for value in values[1:]:

            if value <= end + 15:

                end = value
                touches += 1

            else:

                zones.append({
                    "start": start,
                    "end": end,
                    "touches": touches
                })

                start = value
                end = value
                touches = 1


        zones.append({
            "start": start,
            "end": end,
            "touches": touches
        })


        return zones



    def rank_zones(zones):

        for zone in zones:

            if zone["touches"] >= 10:
                zone["strength"] = "STRONG"

            elif zone["touches"] >= 4:
                zone["strength"] = "MEDIUM"

            else:
                zone["strength"] = "WEAK"


        zones.sort(
            key=lambda x: x["touches"],
            reverse=True
        )


        return zones[:3]



    support_zones = rank_zones(
        build_zones(supports)
    )

    resistance_zones = rank_zones(
        build_zones(resistances)
    )



    return {
        "support": support_zones,
        "resistance": resistance_zones
    }
