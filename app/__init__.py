import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors

# Import models for migration detection
from .models.user import User
from .models.token_blacklist import TokenBlocklist


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # --------------------------
    # Logging Setup
    # --------------------------
    logs_path = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_path, exist_ok=True)

    log_handler = TimedRotatingFileHandler(
        os.path.join(logs_path, "auth.log"),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )

    log_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    log_handler.setLevel(logging.INFO)

    if not any(isinstance(h, TimedRotatingFileHandler) for h in app.logger.handlers):
        app.logger.addHandler(log_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Auth service initializing...")

    # Register routes
    from .api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # JWT revoked token checker
    @jwt.token_in_blocklist_loader
    def token_revoked(jwt_header, jwt_payload):
        from .models.token_blacklist import TokenBlocklist
        jti = jwt_payload.get("jti")
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    app.logger.info("Auth service started successfully.")
    return app
