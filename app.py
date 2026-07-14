from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from ai import analyze_chart
from engine.candle_shapes import detect
from engine.pattern_detector import analyze as analyze_pattern
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "saintscalperfx_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    analyses = conn.execute(
        "SELECT * FROM analyses WHERE user=? ORDER BY created_at DESC",
        (session["user"],)
    ).fetchall()

    conn.close()

    total = len(analyses)

    last_signal = "No analysis yet"
    last_date = "No analysis yet"

    if total > 0:
        last_signal = analyses[0]["signal"]
        last_date = analyses[0]["created_at"]


    buy_count = 0
    sell_count = 0
    wait_count = 0


    for item in analyses:

        if item["signal"] == "BUY":
            buy_count += 1

        elif item["signal"] == "SELL":
            sell_count += 1

        else:
            wait_count += 1


    most_common = "WAIT"

    if buy_count > sell_count and buy_count > wait_count:
        most_common = "BUY"

    elif sell_count > buy_count and sell_count > wait_count:
        most_common = "SELL"



    return render_template(
        "index.html",
        username=session["user"],
        total=total,
        last_signal=last_signal,
        last_date=last_date,
        buy_count=buy_count,
        sell_count=sell_count,
        wait_count=wait_count,
        most_common=most_common
    )



@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]


        conn = get_db()

        try:

            conn.execute(
                "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
                (fullname,email,password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))


        except:

            conn.close()
            return "Account already exists"


    return render_template("signup.html")




@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]


        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        ).fetchone()


        conn.close()


        if user:

            session["user"] = user["fullname"]

            return redirect(url_for("home"))


        return "Invalid login details"


    return render_template("login.html")

@app.route("/settings", methods=["GET","POST"])
def settings():

    if "user" not in session:
        return redirect(url_for("login"))


    conn = get_db()


    if request.method == "POST":

        market = request.form["market"]
        timeframe = request.form["timeframe"]
        risk = request.form["risk"]


        conn.execute(
            """
            INSERT OR REPLACE INTO preferences
            (user, market, timeframe, risk)
            VALUES (?,?,?,?)
            """,
            (
                session["user"],
                market,
                timeframe,
                risk
            )
        )


        conn.commit()


    conn.close()


    return render_template("settings.html")

@app.route("/risk", methods=["GET","POST"])
def risk():

    if "user" not in session:
        return redirect(url_for("login"))


    result = None


    if request.method == "POST":

        balance = float(request.form["balance"])
        risk_percent = float(request.form["risk"])
        pips = float(request.form["pips"])


        risk_amount = balance * (risk_percent / 100)


        result = (
            f"💰 Risk Amount: ${risk_amount:.2f}<br>"
            f"🛑 Stop Loss: {pips} pips<br>"
            f"📊 Risk Level: {risk_percent}%"
        )


    return render_template(
        "risk.html",
        result=result
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))




@app.route("/upload", methods=["POST"])
def upload():


    if "user" not in session:
        return redirect(url_for("login"))


    image = request.files["image"]


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )


    image.save(filepath)



    result = analyze_chart(filepath)
    candle_data = detect(filepath)

    pattern_data = analyze_pattern(
        candle_data["candles"]
    )

    result.update(pattern_data)

    result.update({
        "candle_count": candle_data["candles_found"],
        "candle_bias": candle_data["bias"]
    })



    conn = get_db()


    conn.execute(
        """
        INSERT INTO analyses
        (user, signal, trend, confidence, reason, entry, stop_loss, take_profit, image)
        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            session["user"],
            result["signal"],
            result["trend"],
            result["confidence"],
            result["reason"],
            result["entry"],
            result["stop_loss"],
            result["take_profit"],
            image.filename
        )
    )


    conn.commit()
    conn.close()


    return render_template(
    "result.html",
    signal=result["signal"],
    trend=result["trend"],
    confidence=result["confidence"],
    reason=result["reason"],
    entry=result["entry"],
    stop_loss=result["stop_loss"],
    take_profit=result["take_profit"],
    image=image.filename,
    grade=result["grade"],
    buy_score=result["buy_score"],
    sell_score=result["sell_score"],
    engines=result["engines"],
candle_count=result["candle_count"],
candle_bias=result["candle_bias"],
bullish_candles=result["bullish_candles"],
bearish_candles=result["bearish_candles"],
pattern=result["pattern"],
momentum=result["momentum"]
)




@app.route("/history")
def history():


    if "user" not in session:
        return redirect(url_for("login"))


    conn = get_db()


    data = conn.execute(
        "SELECT * FROM analyses WHERE user=? ORDER BY created_at DESC",
        (session["user"],)
    ).fetchall()


    conn.close()


    return render_template(
        "history.html",
        history=data
    )




@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
