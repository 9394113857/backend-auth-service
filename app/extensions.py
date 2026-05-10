import os
import logging

from logging.handlers import TimedRotatingFileHandler

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail


# =====================================================
# EXTENSIONS
# =====================================================

db = SQLAlchemy()

migrate = Migrate()

jwt = JWTManager()

cors = CORS()

mail = Mail()


# =====================================================
# LOGGING
# =====================================================

def setup_logging(app):

    logs_dir = os.path.join(
        os.getcwd(),
        "logs"
    )

    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(
        logs_dir,
        "auth.log"
    )

    # Avoid duplicate handlers
    if not any(
        isinstance(h, TimedRotatingFileHandler)
        for h in app.logger.handlers
    ):

        handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )

        handler.setFormatter(formatter)

        handler.setLevel(logging.INFO)

        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
