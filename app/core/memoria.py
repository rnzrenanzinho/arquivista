import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[2]
MEMORIA_DIR = BASE_DIR / "data" / "memoria"


def listar_cores() -> list[dict[str, Any]]:
    cores: list[dict[str, Any]] = []

    if not MEMORIA_DIR.exists():
        return cores

    for caminho in sorted(MEMORIA_DIR.glob("*.json")):
        item: dict[str, Any] = {"arquivo": caminho.name}

        try:
            with caminho.open("r", encoding="utf-8") as arquivo:
                payload = json.load(arquivo)

            if isinstance(payload, dict):
                item.update(payload)
            else:
                item.update(
                    {
                        "id": f"ERRO_{caminho.stem.upper()}",
                        "titulo": "CORE inválido",
                        "tipo": "erro",
                        "descricao": "Estrutura JSON inválida: esperado objeto.",
                        "erro": "Conteúdo JSON não é um objeto.",
                    }
                )

        except json.JSONDecodeError as exc:
            item.update(
                {
                    "id": f"ERRO_{caminho.stem.upper()}",
                    "titulo": "CORE inválido",
                    "tipo": "erro",
                    "descricao": "Falha ao interpretar arquivo JSON.",
                    "erro": f"JSON inválido: {exc}",
                }
            )

        cores.append(item)

    return sorted(cores, key=lambda core: str(core.get("id", core.get("arquivo", ""))))


def carregar_core(nome_arquivo: str) -> dict[str, Any] | None:
    caminho = (MEMORIA_DIR / nome_arquivo).resolve()

    try:
        caminho.relative_to(MEMORIA_DIR.resolve())
    except ValueError:
        return None

    if caminho.suffix.lower() != ".json" or not caminho.is_file():
        return None

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            payload = json.load(arquivo)

        if not isinstance(payload, dict):
            return {
                "arquivo": caminho.name,
                "id": f"ERRO_{caminho.stem.upper()}",
                "titulo": "CORE inválido",
                "tipo": "erro",
                "descricao": "Estrutura JSON inválida: esperado objeto.",
                "erro": "Conteúdo JSON não é um objeto.",
            }

        payload["arquivo"] = caminho.name
        return payload

    except json.JSONDecodeError as exc:
        return {
            "arquivo": caminho.name,
            "id": f"ERRO_{caminho.stem.upper()}",
            "titulo": "CORE inválido",
            "tipo": "erro",
            "descricao": "Falha ao interpretar arquivo JSON.",
            "erro": f"JSON inválido: {exc}",
        }
