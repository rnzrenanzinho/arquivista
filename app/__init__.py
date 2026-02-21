from flask import Flask
from config import Config
import os
from .extensions import db, migrate, login_manager, csrf


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Garante pasta instance (SQLite / arquivos locais)
    os.makedirs(app.instance_path, exist_ok=True)

    # Extensões
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para continuar."

    # Blueprints
    from .auth import auth_bp
    from .main import main_bp
    from .finance import finance_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(finance_bp)

    return app