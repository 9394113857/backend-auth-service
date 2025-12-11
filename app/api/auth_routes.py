from flask import Blueprint, request, jsonify, current_app
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

# -------------------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------------------
@auth_bp.get("/")
def health():
    return jsonify({"status": "auth-service UP"}), 200

# -------------------------------------------------------------
# REGISTER
# -------------------------------------------------------------
@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    current_app.logger.info(f"[REGISTER] Attempt email={email}")

    if not email or not password:
        current_app.logger.warning("[REGISTER] Missing fields")
        return jsonify({"message": "email and password required"}), 400

    resp, status = register_user(email, password)

    if status == 201:
        current_app.logger.info(f"[REGISTER] Success email={email}")
    else:
        current_app.logger.warning(f"[REGISTER] Failed email={email} -> {resp}")

    return jsonify(resp), status

# -------------------------------------------------------------
# LOGIN
# -------------------------------------------------------------
@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    current_app.logger.info(f"[LOGIN] Attempt email={email}")

    user = authenticate_user(email, password)
    if not user:
        current_app.logger.warning(f"[LOGIN] Failed email={email}")
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))
    current_app.logger.info(f"[LOGIN] Success user={user.id}")

    return jsonify({"access_token": token}), 200

# -------------------------------------------------------------
# PROFILE
# -------------------------------------------------------------
@auth_bp.get("/profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    current_app.logger.info(f"[PROFILE] user_id={user_id}")
    return jsonify({"user_id": user_id}), 200

# -------------------------------------------------------------
# UPDATE PROFILE
# -------------------------------------------------------------
@auth_bp.put("/profile")
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    new_email = data.get("email")
    new_password = data.get("password")

    current_app.logger.info(f"[UPDATE] user_id={user_id}")

    user = User.query.get(user_id)
    if not user:
        current_app.logger.warning(f"[UPDATE] Not found user_id={user_id}")
        return jsonify({"message": "User not found"}), 404

    if new_email:
        exists = User.query.filter_by(email=new_email).first()
        if exists and exists.id != user.id:
            current_app.logger.warning(f"[UPDATE] Email exists {new_email}")
            return jsonify({"message": "Email already in use"}), 400
        user.email = new_email

    if new_password:
        user.set_password(new_password)

    db.session.commit()
    current_app.logger.info(f"[UPDATE] Success user_id={user_id}")

    return jsonify({"message": "Profile updated successfully"}), 200

# -------------------------------------------------------------
# LOGOUT
# -------------------------------------------------------------
@auth_bp.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    current_app.logger.info(f"[LOGOUT] Revoked jti={jti}")

    return jsonify({"message": "Logged out successfully"}), 200
