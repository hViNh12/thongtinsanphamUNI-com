from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# File lưu ngày
DATE_FILE = "date.txt"

# Lấy ngày hiện tại từ file
def get_date():
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Chưa có ngày"

# Lưu ngày mới
def save_date(new_date):
    with open(DATE_FILE, "w", encoding="utf-8") as f:
        f.write(new_date)

@app.route("/")
def index():
    current_date = get_date()
    return render_template("index.html", ngay=current_date)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        new_date = request.form["ngay"]
        save_date(new_date)
        return redirect(url_for("index"))
    current_date = get_date()
    return render_template("admin.html", ngay=current_date)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
