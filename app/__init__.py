# =====================================================
# 🟦 APP FACTORY – FINAL VERSION (WITH BUILD INFO)
# =====================================================

import os
import logging
import uuid
import json
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify, g, request
from .config import Config
from .extensions import db, migrate, jwt, cors

from .models.user import User
from .models.token_blacklist import TokenBlocklist


# =====================================================
# 🔹 BUILD INFO LOADER (🔥 IMPORTANT)
# =====================================================
def get_build_info():
    try:
        with open("build_info.json") as f:
            return json.load(f)
    except Exception:
        return {"version": "unknown", "commit": "unknown"}


# =====================================================
# 🔹 REQUEST ID FORMATTER
# =====================================================
class RequestFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.request_id = getattr(g, "request_id", "N/A")
        except RuntimeError:
            record.request_id = "N/A"
        return super().format(record)


def create_app(testing: bool = False):
    app = Flask(__name__)

    app.config.from_object(Config)

    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["JWT_SECRET_KEY"] = "test-secret"

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # =====================================================
    # 🔥 REQUEST ID MIDDLEWARE
    # =====================================================
    @app.before_request
    def assign_request_id():
        incoming_id = request.headers.get("X-Request-ID")
        g.request_id = incoming_id if incoming_id else str(uuid.uuid4())

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-ID"] = g.request_id
        return response

    # --------------------------
    # 🔹 Logging
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

    handler.setFormatter(RequestFormatter(
        "%(asctime)s [%(levelname)s] [REQ:%(request_id)s] %(message)s"
    ))

    if not app.logger.handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("🚀 Auth service starting...")

    # --------------------------
    # 🔹 Routes
    # --------------------------
    from .api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # =====================================================
    # 🔥 HEALTH ENDPOINT (FINAL)
    # =====================================================
    @app.get("/")
    def health():
        info = get_build_info()

        app.logger.info(f"[REQ:{g.request_id}] Health check called")

        return jsonify({
            "status": "Auth service running",
            "version": info["version"],
            "commit": info["commit"]
        }), 200

    # --------------------------
    # 🔹 JWT Blacklist
    # --------------------------
    @jwt.token_in_blocklist_loader
    def token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    app.logger.info("✅ Auth service started successfully.")
    return app
