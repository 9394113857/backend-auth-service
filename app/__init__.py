import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt, cors, mail


# ✅ Import models so Alembic detects them
import app.models  # IMPORTANT


def create_app(testing: bool = False):
    app = Flask(__name__)

    # --------------------------
    # Config
    # --------------------------
    app.config.from_object(Config)

    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["JWT_SECRET_KEY"] = "test-secret"

    # --------------------------
    # Extensions
    # --------------------------
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # --------------------------
    # Logging
    # --------------------------
    logs_path = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_path, exist_ok=True)

    handler = TimedRotatingFileHandler(
        os.path.join(logs_path, "auth.log"),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )

    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))

    if not app.logger.handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Auth service starting...")

    # --------------------------
    # Blueprints
    # --------------------------
    from app.api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # --------------------------
    # Health Check
    # --------------------------
    @app.get("/")
    def health():
        return jsonify({"status": "Auth service started successfully."}), 200

    # --------------------------
    # JWT Blocklist
    # --------------------------
    from app.models import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    app.logger.info("Auth service started successfully.")
    return app