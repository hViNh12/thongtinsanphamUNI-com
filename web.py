import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace_this_with_a_secret"  # cần để dùng flash()

# Dùng đường dẫn tuyệt đối (đặt file date.txt cùng thư mục với app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATE_FILE = os.path.join(BASE_DIR, "date.txt")

# Mật khẩu admin (có thể đặt bằng biến môi trường ở production)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "123456")

def get_date():
    try:
        if os.path.exists(DATE_FILE):
            with open(DATE_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception as e:
        app.logger.exception("Lỗi khi đọc file ngày")
    return "Chưa có ngày"

def save_date(new_date):
    try:
        # đảm bảo strip và lưu
        with open(DATE_FILE, "w", encoding="utf-8") as f:
            f.write(new_date.strip())
        app.logger.info("Saved date '%s' to %s", new_date, DATE_FILE)
        return True
    except Exception as e:
        app.logger.exception("Lỗi khi ghi file ngày")
        return False

@app.route("/")
def index():
    current_date = get_date()
    return render_template("index.html", ngay=current_date)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if request.method == "POST":
        new_date = request.form.get("ngay", "").strip()
        password = request.form.get("password", "")

        if password != ADMIN_PASSWORD:
            error = "Sai mật khẩu! Bạn không có quyền cập nhật."
            app.logger.warning("Thử đăng nhập sai mật khẩu từ IP")
        else:
            ok = save_date(new_date)
            if ok:
                flash("Cập nhật ngày thành công.")
                return redirect(url_for("index"))
            else:
                error = "Không thể lưu ngày — kiểm tra quyền/đường dẫn trên server."

    current_date = get_date()
    return render_template("admin.html", ngay=current_date, error=error)

if __name__ == "__main__":
    # debug=True chỉ dùng khi dev
    app.run(host="0.0.0.0", port=5000, debug=True)
