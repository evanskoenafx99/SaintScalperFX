import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from ai import analyze_chart

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "name": "SaintScalperFX API",
        "status": "online"
    })


@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()

    image = data.get("image")

    if not image:
        return jsonify({
            "error": "No chart image provided"
        }), 400

    try:
        result = analyze_chart(image)

        return jsonify({
            "status": "success",
            "analysis": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
