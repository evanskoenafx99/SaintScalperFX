import os
import sys
import requests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify

from engine.ai import SaintScalperBrain
from engine.price_risk import calculate

app = Flask(__name__)

brain = SaintScalperBrain()

latest_market_data = {
    "symbol": "",
    "timeframe": "",
    "bid": 0,
    "ask": 0,
    "candles": []
}

pending_command = {
    "command": "NONE",
    "ticket": 0,
    "lot_size": 0.02,
    "stop_loss": 0,
    "take_profit": 0
}

latest_confirmation = {}

latest_signal = "WAIT"
latest_confidence = 0
latest_analysis = {}

# =========================
# MARKET DATA FROM EA
# =========================

@app.route("/market", methods=["POST"])
def receive_market():

    global latest_market_data
    global latest_signal
    global latest_confidence
    global latest_analysis
    global pending_command

    data = request.get_json(force=True) or {}

    latest_market_data = data

    # Forward market data to the cloud server
    try:
        requests.post(
            "http://127.0.0.1:8000/market",
            json=data,
            timeout=2
        )
    except Exception as e:
        print("Cloud sync failed:", e)

    candles = data.get("candles", [])

    analysis = brain.analyze(candles)
    latest_analysis = analysis

    risk = calculate(
        analysis.get("signal", "WAIT"),
        candles,
        data.get("bid", 0),
        data.get("ask", 0)
    )

    signal = analysis.get("signal", "WAIT")
    confidence = analysis.get("confidence", 0)

    latest_signal = signal
    latest_confidence = confidence

    command = "NONE"

    if signal != "WAIT" and confidence >= 70:
        command = signal

    pending_command = {
        "command": command,
        "ticket": 0,
        "lot_size": risk.get("lot_size", 0.02),
        "stop_loss": risk.get("stop_loss", 0),
        "take_profit": risk.get("take_profit", 0)
    }

    return jsonify({
        "decision": "TRADE" if command != "NONE" else "WAIT",
        "signal": signal,
        "confidence": confidence,
        "stop_loss": pending_command["stop_loss"],
        "take_profit": pending_command["take_profit"],
        "command": command,
        "ticket": pending_command["ticket"],
        "lot_size": pending_command["lot_size"],
        "analysis": analysis
    })


# =========================
# MARKET VIEW
# =========================

@app.route("/market", methods=["GET"])
def get_market():
    return jsonify(latest_market_data)


# =========================
# COMMAND CHANNEL
# =========================

@app.route("/command", methods=["GET"])
def get_command():

    global pending_command

    command = pending_command.copy()

    pending_command = {
        "command": "NONE",
        "ticket": 0,
        "lot_size": 0.02,
        "stop_loss": 0,
        "take_profit": 0
    }

    return jsonify(command)


@app.route("/command", methods=["POST"])
def set_command():

    global pending_command

    pending_command = request.get_json(force=True) or {}

    return jsonify({
        "status": "queued",
        "command": pending_command
    })


# =========================
# EA CONFIRMATION
# =========================

@app.route("/confirmation", methods=["POST"])
def receive_confirmation():

    global latest_confirmation

    latest_confirmation = request.get_json(force=True) or {}

    print("EA CONFIRMATION:")
    print(latest_confirmation)

    return jsonify({
        "status": "received",
        "confirmation": latest_confirmation
    })


@app.route("/confirmation", methods=["GET"])
def get_confirmation():
    return jsonify(latest_confirmation)


# =========================
# APP STATUS
# =========================

@app.route("/status", methods=["GET"])
def get_status():

    return jsonify({
        "cloud": "ONLINE",
        "ai": "READY",
        "worker": "RUNNING",
        "broker": "CONNECTED",
        "signal": latest_signal,
        "confidence": latest_confidence,
        "decision": "TRADE" if latest_signal != "WAIT" else "WAIT",
        "analysis": latest_analysis,
        "symbol": latest_market_data.get("symbol", ""),
        "timeframe": latest_market_data.get("timeframe", ""),
        "balance": 0,
        "equity": 0,
        "open_trades": 0,
        "today_profit": 0
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
