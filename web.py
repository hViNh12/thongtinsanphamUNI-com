from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # cần để flash message

# Cấu hình
UPLOAD_FOLDER = "static"
ADMIN_PASSWORD = "123456"  # đổi theo ý bạn
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Dữ liệu mặc định
DATE_FILE = "date.txt"
CURRENT_IMAGE_NAME = "chuoi.png"  # ảnh mặc định

# ---- Hàm xử lý ngày ----
def get_date():
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Chưa cập nhật"

def save_date(new_date):
    with open(DATE_FILE, "w", encoding="utf-8") as f:
        f.write(new_date)

# ---- Trang chính ----
@app.route("/")
def index():
    current_date = get_date()
    return render_template("index.html", ngay=current_date, image_file=CURRENT_IMAGE_NAME)

# ---- Trang admin ----
@app.route("/admin")
def admin():
    return render_template("admin.html")

# ---- Cập nhật ngày ----
@app.route("/update-date", methods=["POST"])
def update_date():
    password = request.form.get("password", "")
    new_date = request.form.get("new_date", "")

    if password != ADMIN_PASSWORD:
        flash("Sai mật khẩu! Không thể cập nhật ngày.")
        return redirect(url_for("admin"))

    save_date(new_date)
    flash("Cập nhật ngày thành công!")
    return redirect(url_for("index"))

# ---- Đổi ảnh sản phẩm ----
@app.route("/upload-image", methods=["POST"])
def upload_image():
    global CURRENT_IMAGE_NAME
    password = request.form.get("password", "")

    if password != ADMIN_PASSWORD:
        flash("Sai mật khẩu! Không thể đổi ảnh.")
        return redirect(url_for("admin"))

    if "new_image" not in request.files:
        flash("Chưa chọn file ảnh.")
        return redirect(url_for("admin"))

    file = request.files["new_image"]
    if file.filename == "":
        flash("Tên file không hợp lệ.")
        return redirect(url_for("admin"))

    # Lưu ảnh vào static/
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(save_path)

    # Cập nhật tên file đang dùng
    CURRENT_IMAGE_NAME = file.filename
    flash("Đổi ảnh sản phẩm thành công!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
