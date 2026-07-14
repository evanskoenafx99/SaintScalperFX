from PIL import Image


def detect_levels(image_path):

    img = Image.open(image_path).convert("RGB")

    width, height = img.size

    rows = []

    # Scan only chart area
    for y in range(int(height * 0.15), int(height * 0.75)):

        brightness = 0

        for x in range(width):

            r, g, b = img.getpixel((x, y))

            if r > 100 and g > 100 and b > 100:
                brightness += 1

        if brightness > width * 0.15:
            rows.append(y)


    zones = []

    if rows:

        start = rows[0]
        end = rows[0]

        for y in rows[1:]:

            if y <= end + 8:
                end = y

            else:

                zones.append({
                    "start": start,
                    "end": end,
                    "strength": "NORMAL"
                })

                start = y
                end = y


        zones.append({
            "start": start,
            "end": end,
            "strength": "NORMAL"
        })


    # Strength calculation
    for zone in zones:

        size = zone["end"] - zone["start"]

        if size > 15:
            zone["strength"] = "STRONG"

        elif size > 5:
            zone["strength"] = "MEDIUM"


    return {
        "levels_found": len(zones),
        "zones": zones
    }
