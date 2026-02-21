from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None


# ---------------------------
# FINANCEIRO (nível B)
# ---------------------------

class Account(db.Model):
    __tablename__ = "accounts"
    __table_args__ = (
        db.UniqueConstraint("owner_id", "name", name="uq_accounts_owner_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    name = db.Column(db.String(60), nullable=False, index=True)
    kind = db.Column(db.String(20), nullable=False, default="cash")  # cash, bank, card, other
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    owner = db.relationship("User", foreign_keys=[owner_id])


class Category(db.Model):
    __tablename__ = "categories"
    __table_args__ = (
        db.UniqueConstraint("owner_id", "name", name="uq_categories_owner_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    name = db.Column(db.String(60), nullable=False, index=True)
    flow = db.Column(db.String(10), nullable=False)  # income | expense
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    owner = db.relationship("User", foreign_keys=[owner_id])


class BusinessUnit(db.Model):
    __tablename__ = "business_units"
    __table_args__ = (
        db.UniqueConstraint("owner_id", "name", name="uq_business_units_owner_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    name = db.Column(db.String(60), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    owner = db.relationship("User", foreign_keys=[owner_id])


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    flow = db.Column(db.String(10), nullable=False)  # income | expense
    date = db.Column(db.Date, nullable=False, default=date.today)

    amount_cents = db.Column(db.Integer, nullable=False)  # centavos
    currency = db.Column(db.String(3), nullable=False, default="BRL")

    description = db.Column(db.String(200), nullable=True)
    payment_method = db.Column(db.String(30), nullable=True)  # pix, dinheiro, debito, credito...
    reference = db.Column(db.String(60), nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("business_units.id"), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    account = db.relationship("Account")
    category = db.relationship("Category")
    unit = db.relationship("BusinessUnit")
    created_by = db.relationship("User")