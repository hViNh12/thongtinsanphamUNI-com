from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os, time
import qrcode
from io import BytesIO

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Cấu hình ---
UPLOAD_FOLDER = "static"
ADMIN_PASSWORD = "123456"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- File dữ liệu ---
DATE_FILE = "date.txt"
IMAGE_FILE = "image.txt"
DEFAULT_IMAGE = "chuoi.png"

# --- Hàm xử lý ngày ---
def get_date():
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Chưa cập nhật"

def save_date(new_date):
    with open(DATE_FILE, "w", encoding="utf-8") as f:
        f.write(new_date)

# --- Hàm xử lý ảnh ---
def get_image_name():
    if os.path.exists(IMAGE_FILE):
        with open(IMAGE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return DEFAULT_IMAGE

def save_image_name(filename):
    with open(IMAGE_FILE, "w", encoding="utf-8") as f:
        f.write(filename)

# --- Trang chính ---
@app.route("/")
def index():
    current_date = get_date()
    current_image = get_image_name()
    return render_template("index.html", ngay=current_date, image_file=current_image)

# --- Trang admin ---
@app.route("/admin")
def admin():
    return render_template("admin.html")

# --- Cập nhật ngày ---
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

# --- Đổi ảnh sản phẩm ---
@app.route("/upload-image", methods=["POST"])
def upload_image():
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

    # --- Xoá ảnh cũ ---
    old_image = get_image_name()
    old_path = os.path.join(app.config["UPLOAD_FOLDER"], old_image)
    if old_image != DEFAULT_IMAGE and os.path.exists(old_path):
        os.remove(old_path)

    # --- Đặt tên file mới theo timestamp ---
    ext = os.path.splitext(file.filename)[1]
    new_filename = f"product_{int(time.time())}{ext}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)

    file.save(save_path)
    save_image_name(new_filename)

    flash("Đổi ảnh sản phẩm thành công!")
    return redirect(url_for("index"))

# --- Trang QR ---
@app.route("/qr")
def qr_page():
    return render_template("qr.html")

# --- Sinh QR code ---
@app.route("/generate-qr", methods=["POST"])
def generate_qr():
    url = "https://thongtinsanphamUNI-com.onrender.com/"
    qr_img = qrcode.make(url)

    img_io = BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="qr.png")



if __name__ == "__main__":
    app.run(debug=True)
