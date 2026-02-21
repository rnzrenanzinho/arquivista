from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CategoryForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=2, max=60)])
    flow = SelectField("Tipo", choices=[("income", "Entrada"), ("expense", "Saída")], validators=[DataRequired()])
    is_active = BooleanField("Ativa", default=True)
    submit = SubmitField("Salvar")


class AccountForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=2, max=60)])
    kind = SelectField(
        "Tipo",
        choices=[("cash", "Dinheiro"), ("bank", "Banco"), ("card", "Cartão"), ("other", "Outro")],
        validators=[DataRequired()],
    )
    is_active = BooleanField("Ativa", default=True)
    submit = SubmitField("Salvar")


class UnitForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=2, max=60)])
    is_active = BooleanField("Ativa", default=True)
    submit = SubmitField("Salvar")


class TransactionForm(FlaskForm):
    flow = SelectField("Tipo", choices=[("income", "Entrada"), ("expense", "Saída")], validators=[DataRequired()])
    date = DateField("Data", validators=[DataRequired()], format="%Y-%m-%d")
    amount = StringField("Valor (R$)", validators=[DataRequired(), Length(min=1, max=20)])

    unit_id = SelectField("Unidade (Centro de Custo)", coerce=int, validators=[DataRequired()])
    account_id = SelectField("Conta", coerce=int, validators=[DataRequired()])
    category_id = SelectField("Categoria", coerce=int, validators=[DataRequired()])

    payment_method = StringField("Método (pix/dinheiro/cartão)", validators=[Length(max=30)])
    description = StringField("Descrição", validators=[Length(max=200)])
    reference = StringField("Referência", validators=[Length(max=60)])
    submit = SubmitField("Salvar")
