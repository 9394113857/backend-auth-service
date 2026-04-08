# =====================================================
# 🟦 APP FACTORY – FINAL (WITH BUILD METADATA)
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
# 🔥 BUILD INFO LOADER
# =====================================================
def get_build_info():
    try:
        with open("build_info.json") as f:
            return json.load(f)
    except Exception as e:
        return {
            "version": "unknown",
            "commit": "unknown",
            "branch": "unknown",
            "build_time_utc": "unknown",
            "build_time_ist": "unknown",
            "error": str(e)
        }


# =====================================================
# 🔹 REQUEST FORMATTER
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

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # --------------------------
    # 🔥 Request ID Middleware
    # --------------------------
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

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
        backupCount=30,
        encoding="utf-8"
    )

    handler.setFormatter(RequestFormatter(
        "%(asctime)s [%(levelname)s] [REQ:%(request_id)s] %(message)s"
    ))

    if not app.logger.handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)

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

        return jsonify({
            "status": "Auth service running",
            "version": info.get("version"),
            "commit": info.get("commit"),
            "branch": info.get("branch"),
            "build_time_utc": info.get("build_time_utc"),
            "build_time_ist": info.get("build_time_ist")
        }), 200

    return app
