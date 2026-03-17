# =====================================================
# 🟦 AUTH ROUTES – API LAYER (REQUEST/RESPONSE)
# =====================================================

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from ..services.auth_service import register_user
from ..extensions import db
from ..models.token_blacklist import TokenBlocklist
from ..models.user import User

auth_bp = Blueprint("auth", __name__)


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------
@auth_bp.get("/")
def health():
    return jsonify({"status": "auth-service UP"}), 200


# ------------------------------------------------
# REGISTER (USER / SELLER)
# ------------------------------------------------
@auth_bp.post("/angularUser/register")
def angular_register():
    """
    Handles registration request from Angular frontend.
    Delegates DB logic to service layer.
    """

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    # Basic validation 
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    # Call service (handles duplicate + DB logic)
    resp, status = register_user(email, password, role)

    if status != 201:
        return jsonify(resp), status

    current_app.logger.info(
        f"User registered email={email}, role={role}"
    )

    return jsonify(resp), 201


# ------------------------------------------------
# LOGIN
# ------------------------------------------------
@auth_bp.post("/angularUser/login")
def angular_login():
    """
    Authenticates user and returns JWT token.
    """

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    # Fetch user
    user = User.query.filter_by(email=email).first()

    # Validate credentials
    if not user or not user.check_password(password):
        current_app.logger.warning(
            f"Invalid login attempt email={email}"
        )
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate JWT
    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "userId": user.id,
        "role": user.role
    }), 200


# ------------------------------------------------
# PROFILE (PROTECTED ROUTE)
# ------------------------------------------------
@auth_bp.get("/profile")
@jwt_required()
def profile():
    """
    Returns user identity from JWT.
    """
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id}), 200


# ------------------------------------------------
# LOGOUT (TOKEN BLACKLIST)
# ------------------------------------------------
@auth_bp.post("/logout")
@jwt_required()
def logout():
    """
    Invalidates JWT by storing jti in blocklist.
    """
    jti = get_jwt()["jti"]

    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()

    return jsonify({"message": "Logged out successfully"}), 200