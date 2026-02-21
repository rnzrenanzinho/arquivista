from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from .forms import CategoryForm, AccountForm, TransactionForm, UnitForm
from .utils import parse_brl_to_cents, cents_to_brl
from ..extensions import db
from ..models import Category, Account, Transaction, BusinessUnit

finance_bp = Blueprint("finance", __name__)


def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)


def owned_query(model):
    return model.query.filter_by(owner_id=current_user.id)


# =====================
# DASHBOARD PRINCIPAL
# =====================

@finance_bp.route("/finance")
@login_required
def dashboard():
    accounts = owned_query(Account).order_by(Account.name.asc()).all()
    balances = []

    for acc in accounts:
        income = db.session.query(
            func.coalesce(func.sum(Transaction.amount_cents), 0)
        ).filter(
            Transaction.account_id == acc.id,
            Transaction.created_by_id == current_user.id,
            Transaction.flow == "income"
        ).scalar()

        expense = db.session.query(
            func.coalesce(func.sum(Transaction.amount_cents), 0)
        ).filter(
            Transaction.account_id == acc.id,
            Transaction.created_by_id == current_user.id,
            Transaction.flow == "expense"
        ).scalar()

        balance = int(income) - int(expense)
        balances.append({
            "name": acc.name,
            "balance": cents_to_brl(balance)
        })

    return render_template(
        "finance/dashboard.html",
        balances=balances
    )


# =====================
# TRANSAÇÕES
# =====================

@finance_bp.route("/finance/transactions")
@login_required
def transactions():
    rows = Transaction.query.filter_by(created_by_id=current_user.id).order_by(
        Transaction.date.desc(),
        Transaction.id.desc()
    ).all()

    return render_template(
        "finance/transactions.html",
        rows=rows,
        cents_to_brl=cents_to_brl
    )


@finance_bp.route("/finance/transactions/new", methods=["GET", "POST"])
@login_required
def transaction_new():
    units = owned_query(BusinessUnit).filter_by(is_active=True).all()
    accounts = owned_query(Account).filter_by(is_active=True).all()
    categories = owned_query(Category).filter_by(is_active=True).all()

    if not units or not accounts or not categories:
        flash("Crie Unidade, Conta e Categoria antes.", "warning")
        return redirect(url_for("finance.dashboard"))

    form = TransactionForm()

    form.unit_id.choices = [(u.id, u.name) for u in units]
    form.account_id.choices = [(a.id, a.name) for a in accounts]
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        try:
            cents = parse_brl_to_cents(form.amount.data)
        except ValueError:
            flash("Valor inválido. Use formatos como 10,50 ou 1234,56.", "danger")
            return render_template("finance/transaction_form.html", form=form), 400

        selected_unit = owned_query(BusinessUnit).filter_by(
            id=form.unit_id.data,
            is_active=True
        ).first()

        selected_account = owned_query(Account).filter_by(
            id=form.account_id.data,
            is_active=True
        ).first()

        selected_category = owned_query(Category).filter_by(
            id=form.category_id.data,
            is_active=True
        ).first()

        if not selected_unit or not selected_account or not selected_category:
            flash("Seleção inválida. Atualize a página e tente novamente.", "danger")
            return render_template("finance/transaction_form.html", form=form), 400

        if selected_category.flow != form.flow.data:
            flash("A categoria selecionada não corresponde ao tipo da transação.", "danger")
            return render_template("finance/transaction_form.html", form=form), 400

        if cents <= 0:
            flash("O valor da transação deve ser maior que zero.", "danger")
            return render_template("finance/transaction_form.html", form=form), 400

        tx = Transaction(
            flow=form.flow.data,
            date=form.date.data,
            amount_cents=cents,
            unit_id=selected_unit.id,
            account_id=selected_account.id,
            category_id=selected_category.id,
            payment_method=(form.payment_method.data or "").strip() or None,
            description=(form.description.data or "").strip() or None,
            reference=(form.reference.data or "").strip() or None,
            created_by_id=current_user.id,
        )

        db.session.add(tx)
        db.session.commit()

        flash("Transação salva.", "success")
        return redirect(url_for("finance.transactions"))

    return render_template("finance/transaction_form.html", form=form)


# =====================
# CONTAS
# =====================

@finance_bp.route("/finance/accounts")
@login_required
def accounts():
    admin_required()
    rows = owned_query(Account).order_by(Account.name.asc()).all()
    return render_template("finance/accounts.html", rows=rows)


@finance_bp.route("/finance/accounts/new", methods=["GET", "POST"])
@login_required
def account_new():
    admin_required()
    form = AccountForm()

    if form.validate_on_submit():
        a = Account(
            owner_id=current_user.id,
            name=form.name.data.strip(),
            kind=form.kind.data,
            is_active=form.is_active.data,
        )
        try:
            db.session.add(a)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Já existe uma conta com esse nome para este usuário.", "warning")
            return render_template("finance/account_form.html", form=form), 409

        flash("Conta criada.", "success")
        return redirect(url_for("finance.accounts"))

    return render_template("finance/account_form.html", form=form)


# =====================
# CATEGORIAS
# =====================

@finance_bp.route("/finance/categories")
@login_required
def categories():
    admin_required()
    rows = owned_query(Category).order_by(Category.name.asc()).all()
    return render_template("finance/categories.html", rows=rows)


@finance_bp.route("/finance/categories/new", methods=["GET", "POST"])
@login_required
def category_new():
    admin_required()
    form = CategoryForm()

    if form.validate_on_submit():
        c = Category(
            owner_id=current_user.id,
            name=form.name.data.strip(),
            flow=form.flow.data,
            is_active=form.is_active.data,
        )
        try:
            db.session.add(c)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Já existe uma categoria com esse nome para este usuário.", "warning")
            return render_template("finance/category_form.html", form=form), 409

        flash("Categoria criada.", "success")
        return redirect(url_for("finance.categories"))

    return render_template("finance/category_form.html", form=form)


# =====================
# UNIDADES
# =====================

@finance_bp.route("/finance/units")
@login_required
def units():
    admin_required()
    rows = owned_query(BusinessUnit).order_by(BusinessUnit.name.asc()).all()
    return render_template("finance/units.html", rows=rows)


@finance_bp.route("/finance/units/new", methods=["GET", "POST"])
@login_required
def unit_new():
    admin_required()
    form = UnitForm()

    if form.validate_on_submit():
        u = BusinessUnit(
            owner_id=current_user.id,
            name=form.name.data.strip(),
            is_active=form.is_active.data,
        )
        try:
            db.session.add(u)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Já existe uma unidade com esse nome para este usuário.", "warning")
            return render_template("finance/unit_form.html", form=form), 409

        flash("Unidade criada.", "success")
        return redirect(url_for("finance.units"))

    return render_template("finance/unit_form.html", form=form)
