import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("ARQUIVISTA_SECRET_KEY", "dev-change-this-secret-key")

    # Default: SQLite local em /instance/arquivista.sqlite3
    DEFAULT_SQLITE = f"sqlite:///{(BASE_DIR / 'instance' / 'arquivista.sqlite3').as_posix()}"
    SQLALCHEMY_DATABASE_URI = os.environ.get("ARQUIVISTA_DATABASE_URL", DEFAULT_SQLITE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_TIME_LIMIT = None  # evita expirar formulário rápido demais
    