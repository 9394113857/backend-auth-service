# ===============================================================
# AUTH ROUTES
# Handles authentication, profile management and password flows
# ===============================================================

from flask import Blueprint, request, jsonify
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

    if not email or not password or not first_name or not last_name:
        return jsonify({
            "message": "email, password, first_name and last_name required"
        }), 400

    resp, status = register_user(email, password, first_name, last_name)

    return jsonify(resp), status


# =================================================
# VERIFY EMAIL
# =================================================
@auth_bp.get("/angularUser/verify-email/<token>")
def verify_email(token):

    # Find verification token
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

    # Mark email verified
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
# UPDATE PROFILE
# =================================================
@auth_bp.put("/profile")
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json() or {}

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.phone_number = data.get("phone_number", user.phone_number)

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200


# =================================================
# CHANGE PASSWORD (LOGGED-IN USER)
# =================================================
@auth_bp.post("/change-password")
@jwt_required()
def change_password():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.get_json() or {}

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({
            "error": "old_password and new_password required"
        }), 400

    # Verify current password
    if not user.check_password(old_password):
        return jsonify({"error": "Old password incorrect"}), 400

    # ------------------------------------------------
    # PASSWORD HISTORY CHECK (prevent reuse)
    # ------------------------------------------------
    recent = (
        PasswordHistory.query
        .filter_by(user_id=user.id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(10) 
        .all()
    )

    for entry in recent:
        if check_password_hash(entry.password_hash, new_password):
            return jsonify({
                "error": "Cannot reuse a recent password"
            }), 400

    # Update password
    user.set_password(new_password)

    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    db.session.add(history)
    db.session.commit()

    return jsonify({
        "message": "Password changed successfully. Please login again."
    }), 200


# =================================================
# FORGOT PASSWORD
# =================================================
@auth_bp.post("/forgot-password")
def forgot_password():

    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    user = User.query.filter_by(email=email).first()

    # Security practice (avoid user enumeration)
    if not user:
        return jsonify({
            "message": "If email exists reset link sent"
        }), 200

    # ------------------------------------------------
    # IMPORTANT SECURITY:
    # Only ONE reset token per user
    # Delete previous unused tokens
    # ------------------------------------------------
    PasswordResetToken.query.filter_by(
        user_id=user.id,
        is_used=False
    ).delete()

    # Generate new reset token
    token = secrets.token_urlsafe(48)

    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.session.add(reset)
    db.session.commit()

    # Send email
    send_reset_email(user.email, token)

    return jsonify({
        "message": "Password reset email sent"
    }), 200


# =================================================
# RESET PASSWORD
# =================================================
@auth_bp.post("/reset-password/<token>")
def reset_password(token):

    data = request.get_json() or {}
    new_password = data.get("password")

    if not new_password:
        return jsonify({"error": "password required"}), 400

    reset = PasswordResetToken.query.filter_by(
        token=token,
        is_used=False
    ).first()

    if not reset:
        return jsonify({"error": "Invalid token"}), 400

    if reset.expires_at < datetime.utcnow():
        return jsonify({"error": "Token expired"}), 400

    user = User.query.get(reset.user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # ------------------------------------------------
    # PASSWORD HISTORY CHECK (prevent reuse)
    # ------------------------------------------------
    recent = (
        PasswordHistory.query
        .filter_by(user_id=user.id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(5)
        .all()
    )

    for entry in recent:
        if check_password_hash(entry.password_hash, new_password):
            return jsonify({
                "error": "Cannot reuse a recent password"
            }), 400

    # Update password
    user.set_password(new_password)

    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    reset.is_used = True

    db.session.add(history)
    db.session.commit()

    return jsonify({
        "message": "Password reset successful"
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