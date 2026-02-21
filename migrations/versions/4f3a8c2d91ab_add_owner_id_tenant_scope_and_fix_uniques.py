"""add owner_id tenant scope and fix uniques

Revision ID: 4f3a8c2d91ab
Revises: e864077dce64
Create Date: 2026-02-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4f3a8c2d91ab"
down_revision = "e864077dce64"
branch_labels = None
depends_on = None


def _get_fallback_user_id(bind):
    user_id = bind.execute(sa.text("SELECT id FROM users ORDER BY id ASC LIMIT 1")).scalar()
    if user_id is None:
        raise RuntimeError("Não há usuários para vincular owner_id nas tabelas financeiras.")
    return int(user_id)


def upgrade():
    bind = op.get_bind()
    fallback_user_id = _get_fallback_user_id(bind)

    op.add_column("accounts", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.add_column("categories", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.add_column("business_units", sa.Column("owner_id", sa.Integer(), nullable=True))

    bind.execute(sa.text("UPDATE accounts SET owner_id = :uid WHERE owner_id IS NULL"), {"uid": fallback_user_id})
    bind.execute(sa.text("UPDATE categories SET owner_id = :uid WHERE owner_id IS NULL"), {"uid": fallback_user_id})
    bind.execute(sa.text("UPDATE business_units SET owner_id = :uid WHERE owner_id IS NULL"), {"uid": fallback_user_id})

    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.alter_column("owner_id", existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key("fk_accounts_owner_id_users", "users", ["owner_id"], ["id"])
        batch_op.drop_index(batch_op.f("ix_accounts_name"))
        batch_op.create_index(batch_op.f("ix_accounts_name"), ["name"], unique=False)
        batch_op.create_index("ix_accounts_owner_id", ["owner_id"], unique=False)
        batch_op.create_unique_constraint("uq_accounts_owner_name", ["owner_id", "name"])

    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.alter_column("owner_id", existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key("fk_categories_owner_id_users", "users", ["owner_id"], ["id"])
        batch_op.drop_index(batch_op.f("ix_categories_name"))
        batch_op.create_index(batch_op.f("ix_categories_name"), ["name"], unique=False)
        batch_op.create_index("ix_categories_owner_id", ["owner_id"], unique=False)
        batch_op.create_unique_constraint("uq_categories_owner_name", ["owner_id", "name"])

    with op.batch_alter_table("business_units", schema=None) as batch_op:
        batch_op.alter_column("owner_id", existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key("fk_business_units_owner_id_users", "users", ["owner_id"], ["id"])
        batch_op.drop_index(batch_op.f("ix_business_units_name"))
        batch_op.create_index(batch_op.f("ix_business_units_name"), ["name"], unique=False)
        batch_op.create_index("ix_business_units_owner_id", ["owner_id"], unique=False)
        batch_op.create_unique_constraint("uq_business_units_owner_name", ["owner_id", "name"])


def downgrade():
    with op.batch_alter_table("business_units", schema=None) as batch_op:
        batch_op.drop_constraint("uq_business_units_owner_name", type_="unique")
        batch_op.drop_index("ix_business_units_owner_id")
        batch_op.drop_index(batch_op.f("ix_business_units_name"))
        batch_op.create_index(batch_op.f("ix_business_units_name"), ["name"], unique=True)
        batch_op.drop_constraint("fk_business_units_owner_id_users", type_="foreignkey")
        batch_op.drop_column("owner_id")

    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.drop_constraint("uq_categories_owner_name", type_="unique")
        batch_op.drop_index("ix_categories_owner_id")
        batch_op.drop_index(batch_op.f("ix_categories_name"))
        batch_op.create_index(batch_op.f("ix_categories_name"), ["name"], unique=True)
        batch_op.drop_constraint("fk_categories_owner_id_users", type_="foreignkey")
        batch_op.drop_column("owner_id")

    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.drop_constraint("uq_accounts_owner_name", type_="unique")
        batch_op.drop_index("ix_accounts_owner_id")
        batch_op.drop_index(batch_op.f("ix_accounts_name"))
        batch_op.create_index(batch_op.f("ix_accounts_name"), ["name"], unique=True)
        batch_op.drop_constraint("fk_accounts_owner_id_users", type_="foreignkey")
        batch_op.drop_column("owner_id")