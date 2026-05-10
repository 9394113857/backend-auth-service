import os

from flask import Flask, jsonify

from app.config import Config

from app.extensions import (
    db,
    migrate,
    jwt,
    cors,
    mail,
    setup_logging
)

# =====================================================
# IMPORTANT
# Import all models so Alembic detects them
# =====================================================

import app.models


def create_app(testing: bool = False):

    app = Flask(__name__)

    # =====================================================
    # CONFIG
    # =====================================================

    app.config.from_object(Config)

    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["JWT_SECRET_KEY"] = "test-secret"

    # =====================================================
    # EXTENSIONS
    # =====================================================

    cors.init_app(app)

    db.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    mail.init_app(app)

    # =====================================================
    # LOGGING
    # =====================================================

    setup_logging(app)

    app.logger.info("Auth service starting...")

    # =====================================================
    # BLUEPRINTS
    # =====================================================

    from app.api.auth_routes import auth_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/v1/auth"
    )

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @app.get("/")
    def health():
        return jsonify({
            "status": "Auth service started successfully."
        }), 200

    # =====================================================
    # JWT BLOCKLIST
    # =====================================================

    from app.models import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def token_revoked(jwt_header, jwt_payload):

        jti = jwt_payload.get("jti")

        token = TokenBlocklist.query.filter_by(
            jti=jti
        ).first()

        return token is not None

    app.logger.info("Auth service started successfully.")

    return app
