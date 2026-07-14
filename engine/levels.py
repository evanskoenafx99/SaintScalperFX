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

        highs = []
        lows = []


        for y in range(int(height * 0.15), int(height * 0.75)):

            r, g, b = img.getpixel((x, y))

            if r < 80 and g < 80 and b < 80:
                continue

            if r > 100 or g > 100 or b > 100:
                highs.append(y)


        if highs:

            top = min(highs)
            bottom = max(highs)

            resistances.append(top)
            supports.append(bottom)



    def build_zones(values):

        zones = []

        values.sort()

        if not values:
            return zones


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



    support_zones = build_zones(supports)
    resistance_zones = build_zones(resistances)


    return {
        "support": support_zones,
        "resistance": resistance_zones
    }
