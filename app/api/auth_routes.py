# ===============================================================
# AUTH ROUTES
# Handles authentication, profile management and password flows
# Includes production-grade logging
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
    current_app.logger.info("Auth health check requested")
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

    current_app.logger.info(f"Registration attempt email={email}")

    if not email or not password or not first_name or not last_name:

        current_app.logger.warning(
            f"Registration failed - missing fields email={email}"
        )

        return jsonify({
            "message": "email, password, first_name and last_name required"
        }), 400

    resp, status = register_user(email, password, first_name, last_name)

    if status != 201:
        current_app.logger.warning(f"Registration failed email={email}")
    else:
        current_app.logger.info(f"Registration successful email={email}")

    return jsonify(resp), status


# =================================================
# VERIFY EMAIL
# =================================================
@auth_bp.get("/angularUser/verify-email/<token>")
def verify_email(token):

    current_app.logger.info("Email verification attempt")

    record = EmailVerificationToken.query.filter_by(
        token=token,
        is_used=False
    ).first()

    if not record:

        current_app.logger.warning("Email verification failed - invalid token")

        return jsonify({
            "error": "Verification failed or link expired"
        }), 400

    if record.expires_at < datetime.utcnow():

        current_app.logger.warning("Email verification failed - token expired")

        return jsonify({
            "error": "Verification link expired"
        }), 400

    user = User.query.get(record.user_id)

    if not user:

        current_app.logger.error("Email verification failed - user not found")

        return jsonify({"error": "User not found"}), 404

    user.is_verified = True
    record.is_used = True

    db.session.commit()

    current_app.logger.info(f"Email verified user_id={user.id}")

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

    current_app.logger.info(f"Login attempt email={email}")

    if not email or not password:

        current_app.logger.warning("Login failed - missing credentials")

        return jsonify({"message": "email and password required"}), 400

    resp, status = authenticate_user(email, password)

    if status != 200:
        current_app.logger.warning(f"Login failed email={email}")
    else:
        current_app.logger.info(f"Login successful email={email}")

    return jsonify(resp), status


# =================================================
# PROFILE
# =================================================
@auth_bp.get("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    current_app.logger.info(f"Profile requested user_id={user_id}")

    user = User.query.get(user_id)

    if not user or not user.is_active:

        current_app.logger.warning(f"Profile access denied user_id={user_id}")

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

    current_app.logger.info(f"Profile update attempt user_id={user_id}")

    user = User.query.get(user_id)

    if not user:

        current_app.logger.error(f"Profile update failed user_id={user_id}")

        return jsonify({"message": "User not found"}), 404

    data = request.get_json() or {}

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.phone_number = data.get("phone_number", user.phone_number)

    db.session.commit()

    current_app.logger.info(f"Profile updated user_id={user_id}")

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

    current_app.logger.info(f"Password change attempt user_id={user_id}")

    user = User.query.get(user_id)

    data = request.get_json() or {}

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:

        current_app.logger.warning("Password change failed - missing fields")

        return jsonify({
            "error": "old_password and new_password required"
        }), 400

    if not user.check_password(old_password):

        current_app.logger.warning(
            f"Password change failed - wrong old password user_id={user_id}"
        )

        return jsonify({"error": "Old password incorrect"}), 400

    recent = (
        PasswordHistory.query
        .filter_by(user_id=user.id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(10)
        .all()
    )

    for entry in recent:
        if check_password_hash(entry.password_hash, new_password):

            current_app.logger.warning(
                f"Password reuse blocked user_id={user_id}"
            )

            return jsonify({
                "error": "Cannot reuse a recent password"
            }), 400

    user.set_password(new_password)

    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    db.session.add(history)
    db.session.commit()

    current_app.logger.info(f"Password changed user_id={user_id}")

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

    current_app.logger.info(f"Forgot password request email={email}")

    if not email:

        current_app.logger.warning("Forgot password failed - email missing")

        return jsonify({"error": "Email required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:

        current_app.logger.info(
            f"Password reset requested for non-existing email={email}"
        )

        return jsonify({
            "message": "If email exists reset link sent"
        }), 200

    PasswordResetToken.query.filter_by(
        user_id=user.id,
        is_used=False
    ).delete()

    token = secrets.token_urlsafe(48)

    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.session.add(reset)
    db.session.commit()

    send_reset_email(user.email, token)

    current_app.logger.info(
        f"Password reset email sent user_id={user.id}"
    )

    return jsonify({
        "message": "Password reset email sent"
    }), 200


# =================================================
# RESET PASSWORD
# =================================================
@auth_bp.post("/reset-password/<token>")
def reset_password(token):

    current_app.logger.info("Password reset attempt")

    data = request.get_json() or {}
    new_password = data.get("password")

    if not new_password:

        current_app.logger.warning("Reset password failed - missing password")

        return jsonify({"error": "password required"}), 400

    reset = PasswordResetToken.query.filter_by(
        token=token,
        is_used=False
    ).first()

    if not reset:

        current_app.logger.warning("Reset password failed - invalid token")

        return jsonify({"error": "Invalid token"}), 400

    if reset.expires_at < datetime.utcnow():

        current_app.logger.warning("Reset password failed - token expired")

        return jsonify({"error": "Token expired"}), 400

    user = User.query.get(reset.user_id)

    if not user:

        current_app.logger.error("Reset password failed - user not found")

        return jsonify({"error": "User not found"}), 404

    recent = (
        PasswordHistory.query
        .filter_by(user_id=user.id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(5)
        .all()
    )

    for entry in recent:
        if check_password_hash(entry.password_hash, new_password):

            current_app.logger.warning(
                f"Password reuse blocked during reset user_id={user.id}"
            )

            return jsonify({
                "error": "Cannot reuse a recent password"
            }), 400

    user.set_password(new_password)

    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    reset.is_used = True

    db.session.add(history)
    db.session.commit()

    current_app.logger.info(f"Password reset successful user_id={user.id}")

    return jsonify({
        "message": "Password reset successful"
    }), 200


# =================================================
# LOGOUT
# =================================================
@auth_bp.post("/logout")
@jwt_required()
def logout():

    user_id = get_jwt_identity()

    jti = get_jwt()["jti"]

    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    current_app.logger.info(f"User logout user_id={user_id}")

    return jsonify({
        "message": "Logged out successfully"
    }), 200