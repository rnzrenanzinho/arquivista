from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__, template_folder="../templates")


@main_bp.get("/")
def index():
    return render_template("main/index.html")


@main_bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", user=current_user)
