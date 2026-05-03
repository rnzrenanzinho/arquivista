from flask import Blueprint, render_template

from .core.identidade import IDENTIDADE_ARQUIVISTA
from .core.software_imortal import SOFTWARE_IMORTAL

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", identidade=IDENTIDADE_ARQUIVISTA)


@main.route("/mente")
def mente():
    return render_template("mente.html", identidade=IDENTIDADE_ARQUIVISTA)


@main.route("/software-imortal")
def software_imortal():
    return render_template("software_imortal.html", software=SOFTWARE_IMORTAL)
