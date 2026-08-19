from PIL import Image


def detect_chart(filepath):

    image = Image.open(filepath).convert("RGB")

    width, height = image.size

    return {
        "image": image,
        "left": 0,
        "top": 0,
        "right": width,
        "bottom": height,
        "width": width,
        "height": height
    }
