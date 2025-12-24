import os

class Config:
    """
    Base configuration for auth-service.
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # DB (SQLite local, Neon on Render)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///auth.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
