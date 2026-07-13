from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from ai import analyze_chart
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

    if "user" in session:
        return render_template(
            "index.html",
            username=session["user"]
        )

    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (fullname,email,password) VALUES (?,?,?)",
                (fullname,email,password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except:
            conn.close()
            return "Account already exists."

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

        return "Invalid login details."

    return render_template("login.html")


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


    return render_template(
        "result.html",
        signal=result["signal"],
        trend=result["trend"],
        confidence=result["confidence"],
        reason=result["reason"],
        entry=result["entry"],
        stop_loss=result["stop_loss"],
        take_profit=result["take_profit"],
        image=image.filename
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
