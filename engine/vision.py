from PIL import Image

def analyze(filepath):
    try:
        img = Image.open(filepath)

        width, height = img.size

        # Approximate MT5 chart area
        chart = img.crop((
            int(width * 0.05),
            int(height * 0.18),
            int(width * 0.95),
            int(height * 0.88)
        ))

        chart.save("uploads/chart_area.png")

        return {
            "status": "OK",
            "width": width,
            "height": height,
            "chart_width": chart.size[0],
            "chart_height": chart.size[1],
            "chart_file": "uploads/chart_area.png",
            "message": "Chart area extracted successfully."
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
