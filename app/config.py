import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ------------------------------------------------
    # Secrets
    # ------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret")

    # ------------------------------------------------
    # Database
    # ------------------------------------------------
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local fallback
        SQLALCHEMY_DATABASE_URI = "sqlite:///auth.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # ------------------------------------------------
    # JWT
    # ------------------------------------------------
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # ------------------------------------------------
    # Email (GMAIL ONLY)
    # ------------------------------------------------
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # ------------------------------------------------
    # Frontend
    # ------------------------------------------------
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")