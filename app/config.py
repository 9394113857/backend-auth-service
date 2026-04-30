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
    # SECURITY
    # -------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

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
