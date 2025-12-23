from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from ..services.auth_service import register_user, authenticate_user
from ..extensions import db
from ..models.user import User
from ..models.token_blacklist import TokenBlocklist

auth_bp = Blueprint("auth", __name__)

# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------
@auth_bp.get("/")
def health():
    return jsonify({"status": "auth-service UP"}), 200

# ------------------------------------------------
# ANGULAR REGISTER
# ------------------------------------------------
@auth_bp.post("/angularUser/register")
def angular_register():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    resp, status = register_user(email, password)

    if status == 201:
        user = User.query.filter_by(email=email).first()
        user.role = role
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "role": role
        }), 201

    return jsonify(resp), status

# ------------------------------------------------
# ANGULAR LOGIN
# ------------------------------------------------
@auth_bp.post("/angularUser/login")
def angular_login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "userId": user.id,
        "role": user.role
    }), 200

# ------------------------------------------------
# PROFILE
# ------------------------------------------------
@auth_bp.get("/profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id}), 200

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
