from flask import Flask, request, jsonify

app = Flask(__name__)

latest_market_data = {
    "symbol": "",
    "timeframe": "",
    "bid": 0,
    "ask": 0,
    "candles": []
}


@app.route("/market", methods=["POST"])
def receive_market_data():
    global latest_market_data

    data = request.get_json()

    latest_market_data["symbol"] = data.get("symbol", "")
    latest_market_data["timeframe"] = data.get("timeframe", "")
    latest_market_data["bid"] = data.get("bid", 0)
    latest_market_data["ask"] = data.get("ask", 0)
    latest_market_data["candles"] = data.get("candles", [])

    return jsonify({
        "status": "received",
        "candles": len(latest_market_data["candles"])
    })


@app.route("/market", methods=["GET"])
def get_market_data():
    return jsonify(latest_market_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
