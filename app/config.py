# ============================================================
# APPLICATION CONFIGURATION
# Handles environment variables for:
# - Database
# - JWT
# - Mail (Gmail SMTP)
# - Frontend URL
# Works for both LOCAL and RAILWAY deployments
# ============================================================

import os
from datetime import timedelta
from dotenv import load_dotenv

# ------------------------------------------------------------
# Load environment variables from .env (local only)
# Railway automatically injects environment variables
# ------------------------------------------------------------
load_dotenv()


class Config:

    # ========================================================
    # SECRET KEYS
    # ========================================================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret")


    # ========================================================
    # DATABASE CONFIGURATION
    # ========================================================
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local fallback database
        SQLALCHEMY_DATABASE_URI = "sqlite:///auth.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Prevent stale DB connections (important for Railway)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }


    # ========================================================
    # JWT CONFIGURATION
    # ========================================================
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


    # ========================================================
    # EMAIL CONFIGURATION (GMAIL SMTP)
    # ========================================================
    # Used for:
    # - Email verification
    # - Password reset
    # ========================================================

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587

    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Default sender
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


    # ========================================================
    # FRONTEND URL
    # Used for email links
    # ========================================================

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:4200"
    )


    # ========================================================
    # DEBUG HELPERS (OPTIONAL)
    # ========================================================

    # Helps debugging mail issues in logs
    MAIL_DEBUG = False