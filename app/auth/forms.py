from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    password2 = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Criar conta")


class LoginForm(FlaskForm):
    login = StringField("Usuário ou Email", validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Entrar")
