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
                3600
            )

        )

    )


    # =====================================================
    # RESEND EMAIL API
    # =====================================================

    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY"
        # re_Dmd8GKRJ_67HMq4Va9pcd9HB5VtbytxpQ
    )

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
        # practicesession3@gmail.com
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
        # klcw gvyo prqp sazb
    )

    MAIL_DEFAULT_SENDER = os.getenv(

        "MAIL_DEFAULT_SENDER",

        # practicesession3@gmail.com

    )

    # =====================================================
    # CORS
    # =====================================================

    CORS_ALLOWED_ORIGINS = os.getenv(

        "CORS_ALLOWED_ORIGINS",

        "http://localhost:4200"
        
        # "https://scintillating-cheesecake-39e8db.netlify.app"
        


    )

    # =====================================================
    # FRONTEND
    # =====================================================

    FRONTEND_URL = os.getenv(

        "FRONTEND_URL",
        
        "http://localhost:4200"

        # "https://scintillating-cheesecake-39e8db.netlify.app"

    )

    # =====================================================
    # FLASK ENV
    # =====================================================

    FLASK_ENV = os.getenv(

        "FLASK_ENV",

        "development"

    )