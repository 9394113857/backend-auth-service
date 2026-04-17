import os
import json
import uuid
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify, g, request

from .config import Config
from .extensions import db, migrate, jwt, cors
from .models.token_blacklist import TokenBlocklist

# ✅ NEW IMPORT
from .errors.handlers import register_error_handlers


# =====================================================
# 🔧 BUILD INFO
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
# 🧾 LOG FORMATTER WITH REQUEST ID
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
    # ❌ REGISTER ERROR HANDLERS (NEW)
    # =====================================================
    register_error_handlers(app)

    # =====================================================
    # ❤️ HEALTH
    # =====================================================
    @app.get("/")
    def health():
        info = get_build_info()

        if "text/html" in request.headers.get("Accept", ""):
            html = f"""
            <html>
            <head><title>Auth Service</title></head>
            <body>
                <h1>🚀 Auth Service</h1>
                <p>Status: UP</p>
                <p>Version: {info.get("version")}</p>
            </body>
            </html>
            """
            return html, 200

        return jsonify({
            "status": "auth-service UP",
            "build": info
        }), 200

    return app
