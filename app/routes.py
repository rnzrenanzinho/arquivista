import json

from flask import Blueprint, abort, render_template

from .core.identidade import IDENTIDADE_ARQUIVISTA
from .core.memoria import carregar_core, listar_cores
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


@main.route("/memoria")
def memoria():
    cores = listar_cores()
    return render_template("memoria.html", cores=cores)


@main.route("/memoria/<nome_arquivo>")
def memoria_core(nome_arquivo: str):
    core = carregar_core(nome_arquivo)
    if core is None:
        abort(404)

    core_formatado = json.dumps(core, ensure_ascii=False, indent=2)
    return render_template("core_detalhe.html", core=core, core_formatado=core_formatado)
