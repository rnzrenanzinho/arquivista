from __future__ import annotations
from datetime import date
import re

def parse_brl_to_cents(value: str) -> int:
    """
    Aceita formatos como:
    '10', '10.50', '10,50', '1.234,56', '1234,56'
    Retorna centavos como int.
    """
    if value is None:
        raise ValueError("Valor vazio")

    s = value.strip()

    # remove R$, espaços
    s = s.replace("R$", "").strip()

    # se tiver . e , assume padrão BR: '.' milhar e ',' decimal
    if "," in s:
        s = s.replace(".", "")
        s = s.replace(",", ".")
    # agora s deve estar no padrão com ponto decimal
    if not re.fullmatch(r"-?\d+(\.\d{1,2})?", s):
        raise ValueError("Formato de valor inválido")

    negative = s.startswith("-")
    if negative:
        s = s[1:]

    if "." in s:
        whole, dec = s.split(".")
        dec = (dec + "00")[:2]
    else:
        whole, dec = s, "00"

    cents = int(whole) * 100 + int(dec)
    return -cents if negative else cents


def cents_to_brl(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    reais = cents // 100
    cent = cents % 100
    return f"{sign}{reais:,}".replace(",", ".") + f",{cent:02d}"
