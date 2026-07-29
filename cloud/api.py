import sys
import os
import requests

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from flask import Flask, request, jsonify
import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

BRIDGE_URL = os.getenv("BRIDGE_URL", "http://127.0.0.1:5001")

DATABASE = "users.db"

# ======================================
# LIVE MARKET MEMORY
# ======================================

from engine.ai import SaintScalperBrain
from engine.price_risk import calculate

brain = SaintScalperBrain()

latest_market_data = {
    "symbol": "",
    "timeframe": "",
    "bid": 0,
    "ask": 0,
    "candles": []
}

latest_analysis = {}

latest_signal = "WAIT"
latest_confidence = 0

pending_command = {
    "command": "NONE",
    "ticket": 0,
    "lot_size": 0.02,
    "stop_loss": 0,
    "take_profit": 0
}

latest_confirmation = {}

def get_db():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn



def prepare_candles(candles):

    prepared = []

    for candle in candles:

        item = dict(candle)

        if item["close"] > item["open"]:

            item["direction"] = "BULLISH"

        elif item["close"] < item["open"]:

            item["direction"] = "BEARISH"

        else:

            item["direction"] = "UNKNOWN"


        prepared.append(item)


    return prepared



@app.route("/")
def home():

    return jsonify({

        "system": "SaintScalperFX Cloud",
        "status": "ONLINE",
        "version": "1.0"

    })



@app.route("/status")
def status():

    return jsonify({

        "cloud": "ONLINE",

        "ai": "READY",

        "worker": "RUNNING",

        "broker": "CONNECTED",

        "signal": latest_signal,

        "confidence": latest_confidence,

        "decision":
            "TRADE" if latest_signal != "WAIT" else "WAIT",

        "analysis": latest_analysis,

        "symbol":
            latest_market_data.get("symbol", ""),

        "timeframe":
            latest_market_data.get("timeframe", ""),

        "balance": 0,

        "equity": 0,

        "open_trades": 0,

        "today_profit": 0

    })

# ======================================
# LIVE MARKET API
# ======================================

@app.route("/market", methods=["POST"])
def receive_market():

    global latest_market_data
    global latest_analysis
    global latest_signal
    global latest_confidence
    global pending_command

    data = request.get_json(force=True) or {}

    latest_market_data = data

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
        "command": command,
        "signal": signal,
        "confidence": confidence,
        "lot_size": pending_command["lot_size"],
        "stop_loss": pending_command["stop_loss"],
        "take_profit": pending_command["take_profit"],
        "analysis": analysis
    })


@app.route("/command", methods=["GET"])
def get_command():
    return jsonify(pending_command)

@app.route("/command", methods=["POST"])
def send_command():

    global pending_command

    data = request.get_json(force=True) or {}

    command = data.get("command", "NONE")

    pending_command["command"] = command

    return jsonify({
        "status": "QUEUED",
        "command": command
    })

@app.route("/confirmation", methods=["POST"])
def confirm_trade():

    global latest_confirmation

    latest_confirmation = request.get_json(force=True) or {}

    pending_command["command"] = "NONE"

    return jsonify({
        "status": "received"
    })

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")


    if not fullname or not email or not password:

        return jsonify({

            "error":"Missing information"

        }),400



    password_hash = generate_password_hash(password)


    try:

        conn = get_db()

        conn.execute(

            """
            INSERT INTO users
            (fullname,email,password)
            VALUES (?,?,?)
            """,

            (
                fullname,
                email,
                password_hash
            )

        )

        conn.commit()
        conn.close()


        return jsonify({

            "status":"success",
            "message":"Account created"

        })


    except Exception as e:

        return jsonify({

            "status":"error",
            "message":str(e)

        }),500




@app.route("/login", methods=["POST"])
def login():

    data = request.json


    email = data.get("email")
    password = data.get("password")


    conn = get_db()

    user = conn.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    ).fetchone()


    conn.close()


    if not user:

        return jsonify({

            "error":"Invalid login"

        }),401



    if check_password_hash(user["password"], password):

        return jsonify({

            "status":"success",

            "user":{

                "id":user["id"],
                "fullname":user["fullname"],
                "email":user["email"]

            }

        })



    return jsonify({

        "error":"Invalid login"

    }),401




@app.route("/ai/analyze", methods=["POST"])
def ai_analyze():

    try:

        from engine.ai import SaintScalperBrain
        from engine.pattern_detector import analyze as pattern_analyze
        from engine.confidence_filter import evaluate_confidence
        from engine.signal_filter import validate_signal
        from engine.trade_plan import generate_trade_plan



        data = request.json

        candles = data.get("candles")


        if not candles:

            return jsonify({

                "error":"No candle data received"

            }),400



        candles = prepare_candles(candles)



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

            "status":"success",

            "analysis":{

                "signal":final["signal"],
                "confidence":result["confidence"],
                "grade":confidence["grade"],
                "reason":final["reason"],
                "pattern":pattern,
                "trade_plan":trade_plan

            }

        })



    except Exception as e:

        import traceback

        traceback.print_exc()


        return jsonify({

            "status":"error",
            "message":str(e)

        }),500

@app.route("/trade/analyze", methods=["POST"])
def trade_analyze():

    try:

        from core.controller import SaintTradingController


        data = request.json


        candles = data.get("candles")

        user_id = data.get("user_id")


        if not candles:

            return jsonify({

                "error":"No candle data received"

            }),400


        if not user_id:

            return jsonify({

                "error":"No user_id provided"

            }),400



        controller = SaintTradingController()


        analysis = controller.analyze_market(candles)



        execution = controller.process_trade(

            user_id=user_id,

            analysis=analysis

        )



        return jsonify({

            "status":"success",

            "user_id":user_id,

            "analysis":analysis,

            "execution":execution

        })



    except Exception as e:

        import traceback

        traceback.print_exc()


        return jsonify({

            "status":"error",

            "message":str(e)

        }),500


    except Exception as e:

        import traceback

        traceback.print_exc()


        return jsonify({

            "status":"error",

            "message":str(e)

        }),500

@app.route("/account/status/<int:user_id>")
def account_status(user_id):

    try:

        from core.account_manager import SaintAccountManager

        manager = SaintAccountManager()

        status = manager.can_trade(user_id)


        return jsonify({

            "status":"success",

            "user_id":user_id,

            "account_status":status

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500



@app.route("/settings/update", methods=["POST"])
def update_settings():

    try:

        data = request.json


        user_id = data.get("user_id")
        mode = data.get("mode","NORMAL")
        risk = data.get("risk","1%")
        auto_trade = data.get("auto_trade","OFF")


        import sqlite3


        conn = sqlite3.connect("users.db")

        cursor = conn.cursor()


        cursor.execute("""
        INSERT OR REPLACE INTO trading_settings
        (user_id, mode, risk, auto_trade)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            mode,
            risk,
            auto_trade
        ))


        conn.commit()

        conn.close()



        return jsonify({

            "status":"success",

            "message":"Trading settings updated"

        })


    except Exception as e:


        return jsonify({

            "status":"error",

            "message":str(e)

        }),500




@app.route("/subscription/status/<int:user_id>")
def subscription_status(user_id):

    try:

        import sqlite3


        conn = sqlite3.connect("users.db")

        conn.row_factory = sqlite3.Row


        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM subscriptions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,))


        result = cursor.fetchone()


        conn.close()



        if result:

            return jsonify({

                "status":"success",

                "subscription":dict(result)

            })


        return jsonify({

            "status":"success",

            "subscription":{

                "plan":"FREE",

                "status":"INACTIVE"

            }

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500

# ======================================
# SAINT ACCOUNT CONNECTOR API
# ======================================

@app.route("/account/connect", methods=["POST"])
def account_connect():

    try:

        data = request.json

        user_id = data.get("user_id")
        broker = data.get("broker")
        account_type = data.get("account_type")
        account_number = data.get("account_number")


        if not user_id or not broker or not account_type or not account_number:

            return jsonify({
                "status":"error",
                "message":"Missing account information"
            }),400


        conn = sqlite3.connect("users.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO trading_accounts
        (user_id, broker, account_type, account_number, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            broker,
            account_type,
            account_number,
            "CONNECTED"
        ))


        conn.commit()
        conn.close()


        return jsonify({

            "status":"success",

            "message":"Trading account connected"

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500



@app.route("/account/details/<int:user_id>")
def account_details(user_id):

    try:

        conn = sqlite3.connect("users.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM trading_accounts
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,))


        account = cursor.fetchone()

        conn.close()


        if account:

            return jsonify({

                "status":"success",

                "account":dict(account)

            })


        return jsonify({

            "status":"success",

            "account":{

                "status":"DISCONNECTED"

            }

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500




@app.route("/account/disconnect", methods=["POST"])
def account_disconnect():

    try:

        data = request.json

        user_id = data.get("user_id")


        conn = sqlite3.connect("users.db")

        cursor = conn.cursor()


        cursor.execute("""
        UPDATE trading_accounts
        SET status='DISCONNECTED'
        WHERE user_id=?
        """,
        (user_id,))


        conn.commit()
        conn.close()


        return jsonify({

            "status":"success",

            "message":"Account disconnected"

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500
# ======================================
# SAINT SUBSCRIPTION API
# ======================================

@app.route("/subscription/activate", methods=["POST"])
def activate_subscription():

    try:

        data = request.json

        user_id = data.get("user_id")
        plan = data.get("plan", "PRO")


        if not user_id:

            return jsonify({
                "status":"error",
                "message":"Missing user_id"
            }),400


        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO subscriptions
        (user_id, plan, status)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            plan,
            "ACTIVE"
        ))


        conn.commit()
        conn.close()


        return jsonify({

            "status":"success",

            "message":"Subscription activated",

            "plan":plan

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500



@app.route("/subscription/cancel", methods=["POST"])
def cancel_subscription():

    try:

        data = request.json

        user_id = data.get("user_id")


        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()


        cursor.execute("""
        UPDATE subscriptions
        SET status='INACTIVE'
        WHERE user_id=?
        """,
        (user_id,))


        conn.commit()
        conn.close()


        return jsonify({

            "status":"success",

            "message":"Subscription cancelled"

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500

# ======================================
# SAINT EXECUTION QUEUE API
# ======================================

@app.route("/execution/queue", methods=["POST"])
def execution_queue():

    try:

        from execution_queue import ExecutionQueue

        data = request.json

        user_id = data.get("user_id")
        order = data.get("order")


        if not user_id or not order:

            return jsonify({

                "status":"error",
                "message":"Missing user or order data"

            }),400


        queue = ExecutionQueue()

        result = queue.add_order(
            user_id,
            order
        )


        return jsonify(result)


    except Exception as e:

        return jsonify({

            "status":"error",
            "message":str(e)

        }),500




@app.route("/execution/pending")
def execution_pending():

    try:

        from execution_queue import ExecutionQueue


        queue = ExecutionQueue()

        orders = queue.get_pending()


        return jsonify({

            "status":"success",

            "orders":orders

        })


    except Exception as e:

        return jsonify({

            "status":"error",
            "message":str(e)

        }),500
# ======================================
# SAINT EXECUTION WORKER API
# ======================================

@app.route("/execution/process", methods=["POST"])
def execution_process():

    try:

        from execution_worker import ExecutionWorker


        worker = ExecutionWorker()

        results = worker.process_orders()


        return jsonify({

            "status":"success",

            "processed":results

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",
        port=8000

    )
