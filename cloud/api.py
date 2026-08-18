import sys
import os
import requests
import sqlite3
import threading

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from execution_monitor import monitor
from engine.ai_memory import ai_memory

from flask import Flask, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from engine.ai import SaintScalperBrain
from engine.price_risk import calculate


app = Flask(__name__)

BRIDGE_URL = os.getenv("BRIDGE_URL", "http://127.0.0.1:5001")

def get_bridge_account():
    # Mobile/cloud mode: no MT5 bridge required.
    # Keep account values at zero until a live broker connector is available.
    return {
        "balance": 0,
        "equity": 0,
        "open_trades": 0,
        "today_profit": 0
    }

def get_bridge_market():
    # Mobile/cloud mode:
    # Market data is supplied directly through POST /market.
    if latest_market_data.get("candles"):
        return latest_market_data

    return None

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

def refresh_ai():
    # Mobile/cloud mode.
    # /market already receives the live candles and runs the AI.
    # Do not query the MT5 bridge here.
    return latest_analysis

@app.route("/status")
def status():

    refresh_ai()

    account = get_bridge_account()

    return jsonify({
        "cloud": "ONLINE",
        "ai": "READY",
        "worker": "RUNNING",
        "broker": "CONNECTED",
        "signal": latest_signal,
        "confidence": latest_confidence,
        "decision": "TRADE" if latest_signal in ["BUY", "SELL"] and latest_confidence >= 80 else "WAIT",
        "analysis": latest_analysis,
        "symbol": latest_market_data.get("symbol", ""),
        "timeframe": latest_market_data.get("timeframe", ""),
        "balance": account["balance"],
        "equity": account["equity"],
        "open_trades": account["open_trades"],
        "today_profit": account["today_profit"]
    })


# ======================================
# TWELVE DATA LIVE FEED
# ======================================

@app.route("/market/live", methods=["GET"])
def live_market():

    market = latest_market_data
    account = get_bridge_account()

    return jsonify({

        "symbol": market.get("symbol", ""),

        "timeframe": market.get("timeframe", ""),

        "bid": market.get("bid", 0),

        "ask": market.get("ask", 0),

        "candles": market.get("candles", []),

        "signal": latest_signal,

        "confidence": latest_confidence,

        "decision": "TRADE" if latest_signal in ["BUY", "SELL"] and latest_confidence >= 80 else "WAIT",

        "analysis": latest_analysis,

        "broker": "CONNECTED",

        "cloud": "ONLINE",

        "ai": "READY",

        "balance": account["balance"],

        "equity": account["equity"],

        "open_trades": account["open_trades"],

        "today_profit": account["today_profit"]

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

    # ==================================================
    # SAINT ULTRA MULTI-TIMEFRAME MARKET DATA
    #
    # H1  = higher-timeframe directional bias
    # M15 = active ICT/SMC setup timeframe
    # M5  = entry confirmation timeframe
    #
    # M15 remains the legacy "candles" field.
    # ==================================================

    timeframes = data.get("timeframes", {})

    m5_candles = timeframes.get("M5", [])
    m15_candles = timeframes.get("M15", [])
    h1_candles = timeframes.get("H1", [])

    if not m15_candles:
        m15_candles = data.get("candles", [])

    latest_market_data = data

    latest_market_data["timeframes"] = {
        "M5": m5_candles,
        "M15": m15_candles,
        "H1": h1_candles
    }

    candles = m15_candles

    print(
        "MTF MARKET:",
        "M5 =", len(m5_candles),
        "M15 =", len(m15_candles),
        "H1 =", len(h1_candles)
    )

    analysis = brain.analyze(
        candles,
        timeframes={
            "M5": m5_candles,
            "M15": m15_candles,
            "H1": h1_candles
        }
    )

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

    # SIGNAL-ONLY MODE
    # The AI may generate BUY/SELL signals,
    # but no automatic execution command is created.
    command = "NONE"

    pending_command = {
        "command": "NONE",
        "ticket": 0,
        "lot_size": risk.get("lot_size", 0.02),
        "stop_loss": risk.get("stop_loss", 0),
        "take_profit": risk.get("take_profit", 0)
    }

    # ==================================================
    # SAINT ULTRA SIGNAL-ONLY RESPONSE
    #
    # No execution controls are exposed here.
    # The mobile app receives market intelligence only.
    # ==================================================

    return jsonify({
        "decision": "SIGNAL" if signal in ["BUY", "SELL"] else "WAIT",

        "signal": signal,
        "confidence": confidence,

        "bias": analysis.get("bias", "NEUTRAL"),
        "state": analysis.get("state", "WAIT"),
        "reason": analysis.get("reason", ""),

        "multi_timeframe": analysis.get(
            "multi_timeframe",
            {}
        ),

        "structure_context": analysis.get(
            "structure_context",
            {}
        ),

        "liquidity": {
            "event": analysis.get(
                "liquidity_event",
                False
            ),
            "type": analysis.get(
                "liquidity_type",
                "NONE"
            )
        },

        "zone": analysis.get(
            "zone",
            {}
        ),

        "entry_confirmation": analysis.get(
            "entry_confirmation",
            {}
        ),

        "risk": analysis.get(
            "risk",
            {}
        ),

        "intelligence": analysis.get(
            "intelligence",
            {}
        ),

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


# ======================================
# PUSH NOTIFICATIONS
# ======================================

def init_push_tokens_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS push_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            expo_push_token TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


init_push_tokens_table()


@app.route("/notifications/register", methods=["POST"])
def register_push_token():
    try:
        data = request.get_json(force=True) or {}

        user_id = data.get("user_id")
        expo_push_token = data.get("expo_push_token")

        if not user_id or not expo_push_token:
            return jsonify({
                "status": "error",
                "message": "user_id and expo_push_token are required"
            }), 400

        conn = get_db()

        # Verify that the user actually exists.
        user = conn.execute(
            "SELECT id FROM users WHERE id=?",
            (user_id,)
        ).fetchone()

        if not user:
            conn.close()

            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404

        # Update the existing token if it already exists.
        existing = conn.execute(
            """
            SELECT id FROM push_tokens
            WHERE expo_push_token=?
            """,
            (expo_push_token,)
        ).fetchone()

        if existing:

            conn.execute(
                """
                UPDATE push_tokens
                SET user_id=?,
                    updated_at=CURRENT_TIMESTAMP
                WHERE expo_push_token=?
                """,
                (user_id, expo_push_token)
            )

        else:

            conn.execute(
                """
                INSERT INTO push_tokens
                (user_id, expo_push_token)
                VALUES (?,?)
                """,
                (user_id, expo_push_token)
            )

        conn.commit()
        conn.close()

        print(
            f"PUSH TOKEN REGISTERED: user={user_id}"
        )

        return jsonify({
            "status": "success",
            "message": "Push token registered"
        })

    except Exception as e:

        print(
            "PUSH TOKEN REGISTRATION ERROR:",
            e
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/ai/analyze", methods=["POST"])
def ai_analyze():

    try:

        from engine.ai import SaintScalperBrain
        from engine.pattern_detector import analyze as pattern_analyze
        from engine.confidence import calculate
        from engine.signal_filter import validate_signal
        from engine.trade_plan import generate_trade_plan



        data = request.json or {}

        # ==================================================
        # SAINT ULTRA MULTI-TIMEFRAME INPUT
        # H1  = directional bias
        # M15 = institutional setup
        # M5  = entry confirmation
        # ==================================================

        timeframes = data.get("timeframes", {})

        h1_candles = timeframes.get("H1", [])
        m15_candles = timeframes.get("M15", [])
        m5_candles = timeframes.get("M5", [])

        # Legacy compatibility
        if not m15_candles:
            m15_candles = data.get("candles", [])

        if not m15_candles:
            return jsonify({
                "error": "No candle data received"
            }), 400

        h1_candles = prepare_candles(h1_candles)
        m15_candles = prepare_candles(m15_candles)
        m5_candles = prepare_candles(m5_candles)

        brain = SaintScalperBrain()

        result = brain.analyze(
            m15_candles,
            timeframes={
                "H1": h1_candles,
                "M15": m15_candles,
                "M5": m5_candles
            }
        )


        pattern = pattern_analyze(m15_candles)



        confidence = calculate(
            result["engines"]
        )

        if confidence["grade"] in ["A", "A+"]:
            confidence_status = "APPROVED"
        elif confidence["grade"] == "B":
            confidence_status = "CAUTION"
        else:
            confidence_status = "WAIT"



        final = validate_signal(

            result["signal"],
            pattern["pattern"],
            pattern["momentum"],
            confidence_status,
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

                # ==============================================
                # SAINT ULTRA FINAL SIGNAL
                # ==============================================
                "signal": final["signal"],
                "confidence": confidence["confidence"],
                "grade": confidence["grade"],
                "reason": final["reason"],

                # ==============================================
                # INSTITUTIONAL MARKET CONTEXT
                # ==============================================
                "bias": result.get("bias", "NEUTRAL"),
                "state": result.get("state", "WAIT"),

                "multi_timeframe": result.get(
                    "multi_timeframe",
                    {}
                ),

                "structure_context": result.get(
                    "structure_context",
                    {}
                ),

                "liquidity": {
                    "event": result.get(
                        "liquidity_event",
                        False
                    ),
                    "type": result.get(
                        "liquidity_type",
                        "NONE"
                    )
                },

                "zone": result.get(
                    "zone",
                    {}
                ),

                "entry_confirmation": result.get(
                    "entry_confirmation",
                    {}
                ),

                "risk": result.get(
                    "risk",
                    {}
                ),

                "intelligence": result.get(
                    "intelligence",
                    {}
                ),

                # ==============================================
                # LEGACY COMPATIBILITY
                # ==============================================
                "pattern": pattern,
                "trade_plan": trade_plan
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

@app.route("/ai")
def ai_status():

    refresh_ai()

    return jsonify({

        "ai": "ONLINE",

        "symbol": latest_market_data.get("symbol",""),

        "timeframe": latest_market_data.get("timeframe",""),

        "price": latest_market_data.get("bid",0),

        "signal": latest_signal,

        "confidence": latest_confidence,

        "analysis": latest_analysis

    })
# ======================================
# SAINT MOBILE TRADE CONTROL
# ======================================

@app.route("/execution/approve/<int:trade_id>", methods=["POST"])
def approve_trade(trade_id):

    import sqlite3

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE execution_queue
    SET status='APPROVED'
    WHERE id=? AND status='READY'
    """,
    (trade_id,))

    conn.commit()

    conn.close()

    return jsonify({
        "status":"success",
        "message":"Trade approved",
        "trade_id":trade_id
    })


@app.route("/execution/reject/<int:trade_id>", methods=["POST"])
def reject_trade(trade_id):

    import sqlite3

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE execution_queue
    SET status='REJECTED'
    WHERE id=? AND status='READY'
    """,
    (trade_id,))

    conn.commit()

    conn.close()

    return jsonify({
        "status":"success",
        "message":"Trade rejected",
        "trade_id":trade_id
    })
# ======================================
# SAINT OPEN TRADE CONTROL
# ======================================

@app.route("/execution/open/<int:trade_id>", methods=["POST"])
def open_trade(trade_id):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
    SELECT *
    FROM execution_queue
    WHERE id=? AND status='APPROVED'
    """,
    (trade_id,))


    order = cursor.fetchone()


    if not order:
        conn.close()

        return jsonify({
            "status":"error",
            "message":"Trade not found or not approved"
        }),400


    cursor.execute("""
    UPDATE execution_queue
    SET status='OPENED'
    WHERE id=?
    """,
    (trade_id,))


    cursor.execute("""
    INSERT INTO trades
    (
        user_id,
        symbol,
        direction,
        entry,
        exit,
        profit,
        status,
        stop_loss,
        take_profit,
        created_at
    )

    VALUES (?,?,?,?,?,?,?,?,?,?)

    """,
    (
        order["user_id"],
        order["symbol"].replace("/",""),
        order["direction"],
        order["entry"],
        None,
        "0",
        "OPEN",
        order["stop_loss"],
        order["take_profit"],
        datetime.now()
    ))


    new_trade_id = cursor.lastrowid




    conn.commit()
    conn.close()


    return jsonify({

        "status":"success",

        "message":"Trade opened and added to lifecycle",

        "execution_id":trade_id,

        "trade_id":new_trade_id,

        "direction":order["direction"]

    })
@app.route("/execution/monitor", methods=["POST"])
def execution_monitor():

    global latest_market_data

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    refresh_ai()

    market = latest_market_data

    current_price = market.get("bid", 0)

    if current_price == 0:
        conn.close()
        return jsonify({
            "status":"error",
            "message":"No market price available"
        }),400


    cursor.execute("""
    SELECT *
    FROM trades
    WHERE status='OPEN'
    """)

    trades = cursor.fetchall()

    closed = []


    for trade in trades:

        entry = float(trade["entry"])

        stop_loss = trade["stop_loss"]
        take_profit = trade["take_profit"]


        if not stop_loss or not take_profit:
            continue


        stop_loss = float(stop_loss)
        take_profit = float(take_profit)


        close_reason = None


        if trade["direction"] == "BUY":

            if current_price >= take_profit:
                close_reason = "TAKE_PROFIT"

            elif current_price <= stop_loss:
                close_reason = "STOP_LOSS"


        elif trade["direction"] == "SELL":

            if current_price <= take_profit:
                close_reason = "TAKE_PROFIT"

            elif current_price >= stop_loss:
                close_reason = "STOP_LOSS"



        if close_reason:


            if trade["direction"] == "BUY":
                profit = current_price - entry
            else:
                profit = entry - current_price


            cursor.execute("""
            UPDATE trades
            SET
                exit=?,
                profit=?,
                status='CLOSED',
                close_reason=?,
                current_price=?
            WHERE id=?
            """,
            (
                current_price,
                str(round(profit,5)),
                close_reason,
                current_price,
                trade["id"]
            ))

            ai_memory.save_trade({

                "symbol": latest_market_data.get("symbol",""),

                "signal": trade["direction"],

                "confidence": latest_confidence,

                "session": latest_analysis.get("session",""),

                "trend": latest_analysis.get("trend",""),

                "liquidity": latest_analysis.get("liquidity",False),

                "fvg": latest_analysis.get("fvg",False),

                "orderblock": latest_analysis.get("orderblock",False),

                "entry": entry,

                "exit": current_price,

                "profit": profit,

                "result": "WIN" if profit > 0 else "LOSS"

            })

            closed.append({
                "trade_id":trade["id"],
                "reason":close_reason,
                "profit":round(profit,5)
            })


    conn.commit()
    conn.close()


    return jsonify({
        "status":"success",
        "price":current_price,
        "closed":closed
    })

if __name__ == "__main__":

    threading.Thread(
        target=monitor,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=8000
    )
