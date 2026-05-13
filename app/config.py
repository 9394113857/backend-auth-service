import os

from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


class Config:

    # =====================================================
    # SECRETS
    # =====================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-dev-secret"
    )

    SECURITY_PASSWORD_SALT = os.getenv(
        "SECURITY_PASSWORD_SALT",
        "dev-salt"
    )

    # =====================================================
    # DATABASE
    # =====================================================

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    if DATABASE_URL:

        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    else:

        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///auth.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {

        "pool_pre_ping": True,

        "pool_recycle": 300,

    }

    # =====================================================
    # JWT
    # =====================================================

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(

        seconds=int(

            os.getenv(
                "JWT_ACCESS_TOKEN_EXPIRES",
                1800
            )

        )

    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # =====================================================
    # MAIL (OPTIONAL FALLBACK SMTP)
    # =====================================================

    MAIL_SERVER = os.getenv(

        "MAIL_SERVER",

        "smtp.gmail.com"

    )

    MAIL_PORT = int(

        os.getenv(

            "MAIL_PORT",

            587

        )

    )

    MAIL_USE_TLS = os.getenv(

        "MAIL_USE_TLS",

        "True"

    ).lower() == "true"

    MAIL_USE_SSL = os.getenv(

        "MAIL_USE_SSL",

        "False"

    ).lower() == "true"

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.getenv(

        "MAIL_DEFAULT_SENDER",

        MAIL_USERNAME

    )

    # =====================================================
    # CORS
    # =====================================================

    CORS_ALLOWED_ORIGINS = os.getenv(

        "CORS_ALLOWED_ORIGINS",

        "http://localhost:4200"

    )

    # =====================================================
    # FRONTEND
    # =====================================================

    FRONTEND_URL = os.getenv(

        "FRONTEND_URL",
        "http://localhost:4200"
    )
