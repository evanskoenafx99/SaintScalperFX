import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from flask import Flask, request, jsonify

from ai import analyze_chart
from engine.ai import SaintScalperBrain
from engine.pattern_detector import analyze as pattern_analyze
from engine.levels import detect_levels
from engine.trade_plan import generate_trade_plan
from engine.confidence_filter import evaluate_confidence
from engine.signal_filter import validate_signal


app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({
        "name": "SaintScalperFX API",
        "status": "online",
        "mode": "LIVE MT5 READY"
    })


# Existing screenshot analyzer
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



# New MT5 live analyzer
@app.route("/live_signal", methods=["POST"])
def live_signal():

    data = request.get_json()

    candles = data.get("candles")


    if not candles:

        return jsonify({
            "error": "No candles received"
        }), 400


    try:

        brain = SaintScalperBrain()

        result = brain.analyze(candles)


        pattern = pattern_analyze(candles)


        confidence = evaluate_confidence(
            result["confidence"]
        )


        final = validate_signal(
            result["signal"],
            pattern["pattern"],
            pattern["momentum"],
            confidence["status"],
            result["engines"]
        )


        trade_plan = generate_trade_plan(
            final["signal"],
            pattern["pattern"],
            pattern["momentum"],
            {},
            result["engines"]
        )


        return jsonify({

            "status": "success",

            "analysis": {

                "signal": final["signal"],

                "confidence": result["confidence"],

                "grade": confidence["grade"],

                "reason": final["reason"],

                "pattern": pattern,

                "engines": result["engines"],

                "trade_plan": trade_plan

            }

        })


    except Exception as e:


        return jsonify({

            "status": "error",

            "message": str(e)

        }),500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000
    )



