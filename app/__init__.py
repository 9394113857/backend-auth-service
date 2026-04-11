# =====================================================
# 🟦 APP FACTORY – FINAL (TAG + COMMIT METADATA UI)
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
            "commit_short": "unknown",
            "branch": "unknown",
            "tag": "unknown",
            "commit_title": "unknown",
            "commit_body": "No details available",
            "commit_time": "unknown",
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
    # 🔥 HEALTH ENDPOINT (ENHANCED UI)
    # =====================================================
    @app.get("/")
    def health():
        info = get_build_info()

        commit_body = info.get("commit_body") or "No details available"

        html = f"""
        <html>
        <head>
        <title>Auth Service</title>
        <style>
        body {{ font-family: Arial; background:#f4f6f8; }}
        .box {{ max-width:700px;margin:60px auto;background:white;padding:20px;border-radius:10px; }}
        .row {{ margin:8px 0; }}
        .label {{ font-weight:bold; }}
        </style>
        </head>

        <body>
        <div class="box">
        <h2>🚀 Auth Service</h2>
        <div>🟢 Running</div>

        <div class="row"><span class="label">Tag:</span> {info.get("tag")}</div>
        <div class="row"><span class="label">Version:</span> {info.get("version")}</div>

        <div class="row"><span class="label">Commit (7):</span> {info.get("commit_short")}</div>
        <div class="row"><span class="label">Commit (Full):</span> {info.get("commit")}</div>

        <div class="row"><span class="label">Title:</span> {info.get("commit_title")}</div>
        <div class="row"><span class="label">Details:</span><pre>{commit_body}</pre></div>

        <div class="row"><span class="label">Commit Time:</span> {info.get("commit_time")}</div>

        <div class="row"><span class="label">Build UTC:</span> {info.get("build_time_utc")}</div>
        <div class="row"><span class="label">Build IST:</span> {info.get("build_time_ist")}</div>

        </div>
        </body>
        </html>
        """
        return html, 200

    return app
