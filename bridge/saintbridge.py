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

from engine.live_candles import detect as live_detect
from engine.ai import SaintScalperBrain
from engine.price_risk import calculate as calculate_risk
app = Flask(__name__)
brain = SaintScalperBrain()
# =========================
# LIVE MARKET DATA
# =========================
latest_market_data = {
    "symbol": "",
    "timeframe": "",
    "bid": 0.0,
    "ask": 0.0,
    "candles": []
}

# =========================
# LIVE ACCOUNT DATA
# =========================
latest_account_data = {
    "balance": 0.0,
    "equity": 0.0,
    "margin": 0.0,
    "free_margin": 0.0,
    "profit": 0.0,
    "open_trades": 0
}

# =========================
# RECEIVE MARKET DATA
# =========================
@app.route("/market", methods=["POST"])
def receive_market():

    global latest_market_data

    data = request.get_json() or {}

    print("\n========== MARKET RECEIVED ==========")
    print(data)
    print("====================================\n")

    latest_market_data["symbol"] = data.get("symbol", "")
    latest_market_data["timeframe"] = data.get("timeframe", "")
    latest_market_data["bid"] = data.get("bid", 0.0)
    latest_market_data["ask"] = data.get("ask", 0.0)
    latest_market_data["candles"] = data.get("candles", [])

    analysis = brain.analyze(
        latest_market_data["candles"]
    )

    risk = calculate_risk(
        analysis.get("signal","WAIT"),
        latest_market_data["candles"],
        latest_market_data["bid"],
        latest_market_data["ask"]
    )
    confidence = analysis.get("confidence",0)
    signal = analysis.get("signal","WAIT")

    decision = "WAIT"

    if signal != "WAIT" and confidence >= 70:
        decision = "TRADE"

    trade_plan = analysis.get("trade_plan", {})

    return jsonify({
        "decision": decision,
        "signal": signal,
        "confidence": confidence,
        "score": analysis.get("score",0),
        "maximum": analysis.get("maximum",0),
        "stop_loss": risk.get("stop_loss",0),
        "take_profit": risk.get("take_profit",0),
        "grade": analysis.get("grade",""),
        "reason": analysis.get("reason","")
    })


# =========================
# RETURN MARKET + AI
# =========================
@app.route("/market", methods=["GET"])
def get_market():


    live = live_detect(
        latest_market_data["candles"]
    )

    result = brain.analyze(
        live["candles"]
    )

    return jsonify({
        "market": latest_market_data,
        "analysis": result
    })


# =========================
# RECEIVE ACCOUNT DATA
# =========================
@app.route("/account", methods=["POST"])
def receive_account():

    global latest_account_data

    data = request.get_json() or {}

    print("\n========== ACCOUNT RECEIVED ==========")
    print(data)
    print("====================================\n")

    latest_account_data["balance"] = data.get("balance", 0.0)
    latest_account_data["equity"] = data.get("equity", 0.0)
    latest_account_data["margin"] = data.get("margin", 0.0)
    latest_account_data["free_margin"] = data.get("free_margin", 0.0)
    latest_account_data["profit"] = data.get("profit", 0.0)
    latest_account_data["open_trades"] = data.get("open_trades", 0)

    return jsonify({
        "status": "received"
    })


# =========================
# RETURN ACCOUNT
# =========================
@app.route("/account", methods=["GET"])
def get_account():

    return jsonify(latest_account_data)


# =========================
# STATUS
# =========================
@app.route("/status", methods=["GET"])
def status():

    return jsonify({
        "bridge": "online",
        "market": latest_market_data["symbol"],
        "connected": True
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
