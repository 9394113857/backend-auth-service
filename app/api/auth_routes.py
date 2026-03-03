from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from ..services.auth_service import register_user, authenticate_user
from ..extensions import db
from ..models import User, TokenBlocklist

auth_bp = Blueprint("auth", __name__)


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------
@auth_bp.get("/")
def health():
    return jsonify({"status": "auth-service UP"}), 200


# ------------------------------------------------
# REGISTER (first_name & last_name REQUIRED)
# ------------------------------------------------
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


# ------------------------------------------------
# LOGIN
# ------------------------------------------------
@auth_bp.post("/angularUser/login")
def angular_login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    resp, status = authenticate_user(email, password)
    return jsonify(resp), status


# ------------------------------------------------
# PROFILE
# ------------------------------------------------
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
        "role": user.role,
        "is_verified": user.is_verified,
        "created_at": user.created_at
    }), 200


# ------------------------------------------------
# LOGOUT
# ------------------------------------------------
@auth_bp.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200