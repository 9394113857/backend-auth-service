from datetime import timedelta
import os
from dotenv import load_dotenv

# 🔹 Load .env if present (safe)
load_dotenv()


class Config:
    """
    Works for:
    - Local (SQLite)
    - Production (Render + Supabase PostgreSQL)
    """

    # -------------------------------------------------
    # SECURITY KEYS USED FOR JWT AND OTHER ENCRYPTION
    # -------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    
    # -------------------------------------------------
    # This expiration is just for testing. 
    # In production, you would want to set 
    # it to something like 15 minutes or 1 hour.
    # -------------------------------------------------
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=1 # Production: 15 minutes or 1 or 2 hour, depending on your needs
    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=7 # Production: 7 days or more, depending on your needs
    )
    
    # Remember ✅: You can use timedelta to set expiration for access and refresh tokens.
    # Supported directly:
    # timedelta(
    #     weeks=?,
    #     days=?,
    #     hours=?,
    #     minutes=?,
    #     seconds=?,
    #     milliseconds=?,
    #     microseconds=?
    # )
    
    # For months and years, convert them to days:
    # 30 days ≈ 1 month
    # 365 days ≈ 1 year


    # -------------------------------------------------
    # DATABASE
    # -------------------------------------------------
    # Local:
    #   sqlite:///auth.db
    # Supabase:
    #   postgresql://... (from Supabase dashboard)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///auth.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------
    # ✅ STABILITY (GOOD FOR SUPABASE TOO)
    # -------------------------------------------------
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
