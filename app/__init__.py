# =====================================================
# 🟦 APP FACTORY – FINAL (STABLE METADATA UI)
# =====================================================

import os
import logging
import uuid
import json
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, g, request
from .config import Config
from .extensions import db, migrate, jwt, cors

from .models.user import User
from .models.token_blacklist import TokenBlocklist


def get_build_info():
    try:
        path = os.path.join(os.getcwd(), "build_info.json")
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        return {
            "version": "unknown",
            "commit": "unknown",
            "commit_short": "unknown",
            "tag": "unknown",
            "commit_title": "unknown",
            "commit_body": "No details available",
            "commit_time": "unknown",
            "build_time_utc": "unknown",
            "build_time_ist": "unknown",
            "error": str(e)
        }


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

    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-ID"] = g.request_id
        return response

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

    from .api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    @app.get("/")
    def health():
        info = get_build_info()
        body = info.get("commit_body") or "No details available"

        return f"""
        <h2>🚀 Auth Service</h2>
        <p>🟢 Running</p>

        <p><b>Tag:</b> {info.get("tag")}</p>
        <p><b>Version:</b> {info.get("version")}</p>

        <p><b>Commit (7):</b> {info.get("commit_short")}</p>
        <p><b>Commit (Full):</b> {info.get("commit")}</p>

        <p><b>Title:</b> {info.get("commit_title")}</p>
        <pre>{body}</pre>

        <p><b>Commit Time:</b> {info.get("commit_time")}</p>

        <p><b>Build UTC:</b> {info.get("build_time_utc")}</p>
        <p><b>Build IST:</b> {info.get("build_time_ist")}</p>
        """, 200

    return app