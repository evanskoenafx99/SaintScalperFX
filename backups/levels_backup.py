from PIL import Image


def detect_levels(image_path):

    img = Image.open(image_path).convert("RGB")

    width, height = img.size

    levels = []

    for y in range(int(height * 0.15), int(height * 0.75)):

        pixels = []

        for x in range(width):

            r, g, b = img.getpixel((x, y))

            if r > 100 and g > 100 and b > 100:
                pixels.append(x)

        if len(pixels) > width * 0.25:
            levels.append(y)


    zones = []

    if levels:

        start = levels[0]
        end = levels[0]

        for level in levels[1:]:

            if level <= end + 5:
                end = level

            else:
                zones.append({
                    "start": start,
                    "end": end
                })

                start = level
                end = level


        zones.append({
            "start": start,
            "end": end
        })


    return {
        "levels_found": len(zones),
        "zones": zones
    }
