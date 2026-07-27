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
import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

DATABASE = "users.db"


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
        "execution": "WAITING"

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


        if not candles:

            return jsonify({

                "error":"No candle data received"

            }),400



        controller = SaintTradingController()


        analysis = controller.analyze_market(candles)



        execution = controller.process_trade(
            analysis
        )



        return jsonify({

            "status":"success",

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



if __name__ == "__main__":

    app.run(

        host="0.0.0.0",
        port=8000

    )
