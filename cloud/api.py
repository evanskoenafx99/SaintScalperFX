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

from engine.ai_memory import ai_memory

from flask import Flask, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from engine.ai import SaintScalperBrain
from engine.price_risk import calculate


app = Flask(__name__)

# SAINT ULTRA has no MT5 bridge or execution layer.

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
    return jsonify({
        "cloud": "ONLINE",
        "ai": "READY",
        "service": "SAINT_ULTRA",
        "signal": latest_signal,
        "confidence": latest_confidence,
        "analysis": latest_analysis,
        "symbol": latest_market_data.get("symbol", ""),
        "timeframe": latest_market_data.get("timeframe", "")
    })

@app.route("/market/live", methods=["GET"])
def live_market():
    market = latest_market_data

    return jsonify({
        "symbol": market.get("symbol", ""),
        "timeframe": market.get("timeframe", ""),
        "bid": market.get("bid", 0),
        "ask": market.get("ask", 0),
        "candles": market.get("candles", []),
        "signal": latest_signal,
        "confidence": latest_confidence,
        "analysis": latest_analysis,
        "cloud": "ONLINE",
        "ai": "READY"
    })

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


        # ==================================================
        # SAINT ULTRA FINAL DECISION
        #
        # SaintScalperBrain is the SINGLE authority for
        # the final directional signal.
        #
        # Removed from this live route:
        #   pattern_detector
        #   confidence.py
        #   signal_filter.py
        #
        # The upgraded brain result now flows directly
        # into the upgraded SAINT ULTRA trade plan.
        # ==================================================

        brain_signal = str(
            result.get("signal", "WAIT")
        ).upper()

        candidate_signal = (
            brain_signal
            if brain_signal in ("BUY", "SELL")
            else "WAIT"
        )

        trade_plan = generate_trade_plan(
            candidate_signal,
            result,
            price=(
                m5_candles[-1].get("close", 0)
                if m5_candles
                else 0
            )
        )

        # ==================================================
        # STRUCTURAL TRADE GATE
        #
        # A directional brain signal is only a CANDIDATE.
        #
        # The final public signal requires:
        #   SL
        #   TP
        #   valid geometry
        #   acceptable RR
        #
        # Otherwise the final signal is WAIT.
        # ==================================================

        trade_valid = (
            trade_plan.get("trade_valid") is True
        )

        # ==================================================
        # FINAL SIGNAL AUTHORITY
        #
        # Brain direction is only a candidate.
        # The structural trade plan decides whether
        # BUY/SELL can become the public signal.
        # ==================================================

        final_signal = (
            candidate_signal
            if trade_valid
            else "WAIT"
        )

        if final_signal == "WAIT":
            trade_plan["signal"] = "WAIT"

        # ==================================================
        # FINAL CONFIDENCE → GRADE
        #
        # Grade is ALWAYS derived from final confidence.
        # Invalid trade plans cannot publish confidence.
        # ==================================================

        try:
            final_confidence = float(
                result.get("confidence", 0)
            )
        except (TypeError, ValueError):
            final_confidence = 0

        if not trade_valid:
            final_confidence = 0

        final_confidence = max(
            0,
            min(100, round(final_confidence))
        )

        if final_confidence >= 90:
            final_grade = "A+"
        elif final_confidence >= 80:
            final_grade = "A"
        elif final_confidence >= 70:
            final_grade = "B"
        elif final_confidence >= 60:
            final_grade = "C"
        else:
            final_grade = "D"

        return jsonify({
            "status": "success",
            "analysis": {

                # ==============================================
                # SAINT ULTRA FINAL SIGNAL
                # ==============================================
                "signal": final_signal,
                "confidence": final_confidence,
                "grade": final_grade,
                "reason": (
                    trade_plan.get("reason", "")
                    if not trade_valid
                    else result.get("reason", "")
                ),

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

if __name__ == "__main__":

    threading.Thread(
        target=monitor,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=8000
    )
