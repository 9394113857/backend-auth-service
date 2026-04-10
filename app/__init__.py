# =====================================================
# 🟦 APP FACTORY – FINAL (WITH SIMPLE HEALTH UI)
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
    # 🔥 HEALTH ENDPOINT (SIMPLE HTML UI)
    # =====================================================
    @app.get("/")
    def health():
        info = get_build_info()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Auth Service Health</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f4f6f8;
                    margin: 0;
                    padding: 0;
                    color: #333;
                }}

                .container {{
                    max-width: 600px;
                    margin: 80px auto;
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}

                h1 {{
                    text-align: center;
                    color: #1a73e8;
                    margin-bottom: 20px;
                }}

                .status {{
                    text-align: center;
                    font-weight: bold;
                    color: green;
                    margin-bottom: 20px;
                }}

                .row {{
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                    display: flex;
                    justify-content: space-between;
                }}

                .label {{
                    font-weight: bold;
                    color: #555;
                }}

                .value {{
                    color: #222;
                    word-break: break-word;
                }}

                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #999;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <h1>🚀 Auth Service</h1>

                <div class="status">🟢 Service Running</div>

                <div class="row">
                    <div class="label">Version</div>
                    <div class="value">{info.get("version")}</div>
                </div>

                <div class="row">
                    <div class="label">Commit</div>
                    <div class="value">{info.get("commit")}</div>
                </div>

                <div class="row">
                    <div class="label">Branch</div>
                    <div class="value">{info.get("branch")}</div>
                </div>

                <div class="row">
                    <div class="label">Build UTC</div>
                    <div class="value">{info.get("build_time_utc")}</div>
                </div>

                <div class="row">
                    <div class="label">Build IST</div>
                    <div class="value">{info.get("build_time_ist")}</div>
                </div>

                <div class="footer">
                    Built with Flask • Health Check Endpoint
                </div>
            </div>
        </body>
        </html>
        """

        return html, 200

    return app