# ===============================================================
# AUTH ROUTES
# Handles authentication, profile management and password flows
# ===============================================================

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from datetime import datetime, timedelta
import secrets
from werkzeug.security import check_password_hash

from ..services.auth_service import register_user, authenticate_user
from ..services.email_service import send_reset_email
from ..extensions import db
from ..models import (
    User,
    TokenBlocklist,
    PasswordHistory,
    PasswordResetToken,
    EmailVerificationToken
)

auth_bp = Blueprint("auth", __name__)


# =================================================
# HEALTH CHECK
# =================================================
@auth_bp.get("/")
def health():
    return jsonify({"status": "auth-service UP"}), 200


# =================================================
# REGISTER USER
# =================================================
@auth_bp.post("/angularUser/register")
def angular_register():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    # 🔥 NEW
    role_type = data.get("role_type", "user")

    if not email or not password or not first_name or not last_name:
        return jsonify({
            "message": "email, password, first_name and last_name required"
        }), 400

    resp, status = register_user(
        email,
        password,
        first_name,
        last_name,
        role_type   # 🔥 PASS ROLE
    )

    return jsonify(resp), status


# =================================================
# VERIFY EMAIL
# =================================================
@auth_bp.get("/angularUser/verify-email/<token>")
def verify_email(token):

    record = EmailVerificationToken.query.filter_by(
        token=token,
        is_used=False
    ).first()

    if not record:
        return jsonify({
            "error": "Verification failed or link expired"
        }), 400

    if record.expires_at < datetime.utcnow():
        return jsonify({
            "error": "Verification link expired"
        }), 400

    user = User.query.get(record.user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_verified = True
    record.is_used = True

    db.session.commit()

    return jsonify({
        "message": "Email verified successfully"
    }), 200


# =================================================
# LOGIN
# =================================================
@auth_bp.post("/angularUser/login")
def angular_login():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    resp, status = authenticate_user(email, password)

    return jsonify(resp), status


# =================================================
# PROFILE
# =================================================
@auth_bp.get("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_active:
        return jsonify({"message": "User not active"}), 403

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "role": user.role,
        "is_verified": user.is_verified,
        "created_at": user.created_at
    }), 200


# =================================================
# LOGOUT
# =================================================
@auth_bp.post("/logout")
@jwt_required()
def logout():

    jti = get_jwt()["jti"]

    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    return jsonify({
        "message": "Logged out successfully"
    }), 200