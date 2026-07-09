# =====================================================
# 🟦 AUTH ROUTES – API LAYER (REQUEST/RESPONSE)  
# =====================================================

from flask import Blueprint, request, jsonify, current_app, g
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    decode_token
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

    current_app.logger.info(
        "Health check called"
    )

    return jsonify({
        "status": "auth-service UP",
        "request_id": g.request_id
    }), 200

# This is a test route to trigger an error and verify logging:-  
@auth_bp.route("/sentry-test", methods=["GET"])
def sentry_test():
    return 1 / 0  # This will raise a ZeroDivisionError and should be captured by Sentry


# ------------------------------------------------
# REGISTER
# ------------------------------------------------
@auth_bp.post("/angularUser/register")
def angular_register():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        current_app.logger.warning(f"[REQ:{g.request_id}] Missing email/password")
        return jsonify({"message": "email and password required"}), 400

    resp, status = register_user(email, password, role)

    if status != 201:
        current_app.logger.warning(f"[REQ:{g.request_id}] Duplicate user {email}")
        return jsonify(resp), status

    current_app.logger.info(
        f"[REQ:{g.request_id}] User registered email={email}, role={role}"
    )

    return jsonify(resp), 201


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

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        current_app.logger.warning(
            f"[REQ:{g.request_id}] Invalid login {email}"
        )
        return jsonify({"message": "Invalid email or password"}), 401

    # These tokens are created with the user's ID as the identity. 
    # You can also include additional claims if needed.
    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    current_app.logger.info(
        f"[REQ:{g.request_id}] Login success user_id={user.id}"
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
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

    current_app.logger.info(
        f"[REQ:{g.request_id}] Profile accessed user_id={user_id}"
    )

    return jsonify({
        "user_id": user_id
    }), 200
    
# ------------------------------------------------
# REFRESH TOKEN
# ------------------------------------------------
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():

    print("REFRESH ROUTE HIT")
    
    user_id = get_jwt_identity()

    access_token = create_access_token(
        identity=user_id
    )

    current_app.logger.info(
        f"[REQ:{g.request_id}] Refresh token used user_id={user_id}"
    )

    return jsonify({
        "access_token": access_token
    }), 200


# ------------------------------------------------
# LOGOUT ROUTE
# ------------------------------------------------
@auth_bp.post("/logout")
@jwt_required()
def logout():

    data = request.get_json(
        silent=True
    ) or {}

    refresh_token = data.get(
        "refresh_token"
    )

    # Blacklist access token
    access_jti = get_jwt()["jti"]

    db.session.add(
        TokenBlocklist(jti=access_jti)
    )

    # Blacklist refresh token
    if refresh_token:
        try:

            decoded = decode_token(
                refresh_token
            )

            refresh_jti = decoded["jti"]

            db.session.add(
                TokenBlocklist(jti=refresh_jti)
            )

        except Exception:

            current_app.logger.warning(
                f"[REQ:{g.request_id}] Invalid refresh token during logout"
            )

    db.session.commit()

    current_app.logger.info(
        f"[REQ:{g.request_id}] Logout successful"
    )

    return jsonify({
        "message": "Successfully logged out"
    }), 200


# =====================================================
# 🔧 DEBUG STEPS (UPDATED)
# =====================================================

# 1. Trigger API (Angular/Postman)
# 2. Check logs:
#    logs/auth.log
# 3. Observe:
#    [REQ:<ID>] same for entire request
# 4. Use ID to trace full flow
