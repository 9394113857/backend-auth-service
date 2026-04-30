import os
import json
import uuid
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify, g, request

from .config import Config
from .extensions import db, migrate, jwt, cors
from .models.token_blacklist import TokenBlocklist

from .errors.handlers import register_error_handlers

# =====================================================
# 🚀 SENTRY
# =====================================================
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sentry():
    dsn = os.environ.get("SENTRY_DSN")
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )


# =====================================================
# 🔧 BUILD INFO (READ ONLY)
# =====================================================
def get_build_info():
    try:
        with open("build_info.json") as f:
            return json.load(f)
    except Exception:
        return {
            "version": "unknown",
            "commit": "unknown",
            "branch": "unknown",
            "build_time_utc": "unknown",
            "build_time_ist": "unknown"
        }


# =====================================================
# 🧾 LOG FORMATTER
# =====================================================
class RequestFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.request_id = getattr(g, "request_id", "N/A")
        except RuntimeError:
            record.request_id = "N/A"
        return super().format(record)


# =====================================================
# 🚀 APP FACTORY
# =====================================================
def create_app(testing: bool = False):
    app = Flask(__name__)
    app.config.from_object(Config)

    init_sentry()

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # =====================================================
    # 🔐 JWT BLOCKLIST
    # =====================================================
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    # =====================================================
    # 🆔 REQUEST ID
    # =====================================================
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-ID"] = g.request_id
        return response

    # =====================================================
    # 📂 LOGGING
    # =====================================================
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

    # =====================================================
    # 📦 ROUTES
    # =====================================================
    from .api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # =====================================================
    # ❌ ERROR HANDLERS
    # =====================================================
    register_error_handlers(app)

    # =====================================================
    # ❤️ HEALTH (HTML + JSON)
    # =====================================================
    @app.get("/")
    def health():
        info = get_build_info()

        # HTML (browser)
        if "text/html" in request.headers.get("Accept", ""):
            return f"""
            <html>
            <head>
                <title>🚀 Auth Service</title>
                <style>
                    body {{
                        font-family: Arial;
                        background: #0f172a;
                        color: white;
                        text-align: center;
                        padding-top: 60px;
                    }}
                    .card {{
                        background: #1e293b;
                        padding: 30px;
                        border-radius: 12px;
                        display: inline-block;
                        box-shadow: 0 0 20px rgba(0,0,0,0.5);
                    }}
                    h1 {{ color: #38bdf8; }}
                    .ok {{ color: #22c55e; }}
                    .label {{ color: #94a3b8; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🚀 Auth Service</h1>
                    <p class="ok">🟢 UP</p>

                    <p><span class="label">Version:</span> {info.get("version")}</p>
                    <p><span class="label">Commit:</span> {info.get("commit")}</p>
                    <p><span class="label">Branch:</span> {info.get("branch")}</p>
                    <p><span class="label">UTC:</span> {info.get("build_time_utc")}</p>
                    <p><span class="label">IST:</span> {info.get("build_time_ist")}</p>
                </div>
            </body>
            </html>
            """, 200

        # JSON (API)
        return jsonify({
            "status": "auth-service UP",
            "build": info
        }), 200

    return app
