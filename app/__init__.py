# ============================================================
# APPLICATION FACTORY
# Creates and configures the Flask application
# ============================================================

import os
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify, request, g
from app.config import Config
from app.extensions import db, migrate, jwt, cors, mail

# IMPORTANT
# Import models so Alembic detects them for migrations
import app.models


# ============================================================
# CREATE APP FUNCTION
# ============================================================
def create_app(testing: bool = False):

    app = Flask(__name__)

    # --------------------------------------------------------
    # LOAD CONFIGURATION
    # --------------------------------------------------------
    app.config.from_object(Config)

    # Testing configuration (used for unit tests)
    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["JWT_SECRET_KEY"] = "test-secret"

    # --------------------------------------------------------
    # INITIALIZE EXTENSIONS
    # --------------------------------------------------------
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # ========================================================
    # LOGGING SETUP
    # ========================================================
    # Logs will be stored in logs/auth.log
    # Rotates every midnight and keeps 30 days history
    # ========================================================

    logs_path = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_path, exist_ok=True)

    handler = TimedRotatingFileHandler(
        os.path.join(logs_path, "auth.log"),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)

    app.logger.info("Auth service starting...")

    # ========================================================
    # REQUEST ID TRACING
    # ========================================================
    # Each request gets a unique ID
    # This helps track logs across multiple services
    #
    # Example log:
    # [REQ-12ab3c] POST /login
    # ========================================================

    @app.before_request
    def start_request():

        # Generate unique request ID
        g.request_id = f"REQ-{uuid.uuid4().hex[:8]}"

        app.logger.info(
            f"[{g.request_id}] Request started: {request.method} {request.path}"
        )

    # --------------------------------------------------------
    # AFTER REQUEST LOGGING
    # --------------------------------------------------------
    @app.after_request
    def end_request(response):

        app.logger.info(
            f"[{g.request_id}] Request finished: {response.status}"
        )

        # Send request ID back to client
        response.headers["X-Request-ID"] = g.request_id

        return response

    # ========================================================
    # REGISTER BLUEPRINTS
    # ========================================================
    from app.api.auth_routes import auth_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/v1/auth"
    )

    # ========================================================
    # HEALTH CHECK ROUTE
    # ========================================================
    # Used by Railway / Docker / Load balancers
    # ========================================================

    @app.get("/")
    def health():

        app.logger.info("Health check endpoint called")

        return jsonify({
            "status": "Auth service started successfully."
        }), 200

    # ========================================================
    # JWT TOKEN BLOCKLIST CHECK
    # ========================================================
    # Ensures logged-out tokens cannot be reused
    # ========================================================

    from app.models import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def token_revoked(jwt_header, jwt_payload):

        jti = jwt_payload.get("jti")

        return TokenBlocklist.query.filter_by(
            jti=jti
        ).first() is not None

    app.logger.info("Auth service started successfully.")

    return app