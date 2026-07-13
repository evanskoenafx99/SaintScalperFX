from flask import Flask, render_template, request, send_from_directory
from ai import analyze_chart
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return "No image selected."

    image = request.files["image"]

    if image.filename == "":
        return "No file selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
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
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
