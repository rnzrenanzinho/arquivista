from urllib.parse import urljoin, urlparse

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


def _is_safe_next_url(target: str | None) -> bool:
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@auth_bp.get("/register")
def register():
    form = RegisterForm()
    return render_template("auth/register.html", form=form)


@auth_bp.post("/register")
def register_post():
    form = RegisterForm()
    if not form.validate_on_submit():
        flash("Verifique os campos e tente novamente.", "danger")
        return render_template("auth/register.html", form=form), 400

    username = form.username.data.strip()
    email = form.email.data.strip().lower()

    exists = User.query.filter(or_(User.username == username, User.email == email)).first()
    if exists:
        flash("Usuário ou email já existe.", "warning")
        return render_template("auth/register.html", form=form), 409

    user = User(username=username, email=email)
    user.set_password(form.password.data)

    if User.query.count() == 0:
        user.is_admin = True

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Usuário ou email já existe.", "warning")
        return render_template("auth/register.html", form=form), 409

    flash("Conta criada. Faça login.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.get("/login")
def login():
    form = LoginForm()
    return render_template("auth/login.html", form=form)


@auth_bp.post("/login")
def login_post():
    form = LoginForm()
    if not form.validate_on_submit():
        flash("Dados inválidos.", "danger")
        return render_template("auth/login.html", form=form), 400

    login_value = form.login.data.strip()
    user = User.query.filter(
        or_(User.username == login_value, User.email == login_value.lower())
    ).first()

    if not user or not user.check_password(form.password.data):
        flash("Login ou senha incorretos.", "danger")
        return render_template("auth/login.html", form=form), 401

    login_user(user, remember=True)
    next_url = request.args.get("next")

    if _is_safe_next_url(next_url):
        return redirect(next_url)

    return redirect(url_for("main.dashboard"))


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("main.index"))