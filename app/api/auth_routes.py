# =====================================================
# AUTH ROUTES – API LAYER
# =====================================================

from flask import Blueprint, request, jsonify, current_app, g
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    decode_token,
)

from ..services.auth_service import register_user
from ..extensions import db
from ..models.token_blacklist import TokenBlocklist
from ..models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/")
def health():
    current_app.logger.info("Health check called")
    return jsonify({"status": "auth-service UP", "request_id": g.request_id}), 200


@auth_bp.route("/sentry-test", methods=["GET"])
def sentry_test():
    return 1 / 0


@auth_bp.post("/angularUser/register")
def angular_register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    requested_role = data.get("role")

    if not email or not password:
        current_app.logger.warning(f"[REQ:{g.request_id}] Missing email/password")
        return jsonify({"message": "email and password required"}), 400

    # Public registration must never grant privileged roles.
    if requested_role not in (None, "", "user"):
        return jsonify({
            "message": "Role assignment is restricted. New accounts are registered as user."
        }), 403

    resp, status = register_user(email, password, role="user")
    if status != 201:
        current_app.logger.warning(f"[REQ:{g.request_id}] Registration rejected for {email}")
        return jsonify(resp), status

    current_app.logger.info(
        f"[REQ:{g.request_id}] User registered email={email}, role=user"
    )
    return jsonify(resp), 201


@auth_bp.post("/angularUser/login")
def angular_login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        current_app.logger.warning(f"[REQ:{g.request_id}] Invalid login {email}")
        return jsonify({"message": "Invalid email or password"}), 401

    claims = {"role": user.role or "user"}
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=claims,
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    current_app.logger.info(
        f"[REQ:{g.request_id}] Login success user_id={user.id}, role={user.role}"
    )
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "userId": user.id,
        "role": user.role or "user",
    }), 200


@auth_bp.get("/profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if user is None:
        return jsonify({"message": "User not found"}), 404

    current_app.logger.info(
        f"[REQ:{g.request_id}] Profile accessed user_id={user_id}"
    )
    return jsonify({"user_id": user_id, "role": user.role or "user"}), 200


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if user is None:
        return jsonify({"message": "User not found"}), 404

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role or "user"},
    )
    current_app.logger.info(
        f"[REQ:{g.request_id}] Refresh token used user_id={user_id}"
    )
    return jsonify({"access_token": access_token}), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    data = request.get_json(silent=True) or {}
    refresh_token = data.get("refresh_token")

    db.session.add(TokenBlocklist(jti=get_jwt()["jti"]))
    if refresh_token:
        try:
            decoded = decode_token(refresh_token)
            db.session.add(TokenBlocklist(jti=decoded["jti"]))
        except Exception:
            current_app.logger.warning(
                f"[REQ:{g.request_id}] Invalid refresh token during logout"
            )

    db.session.commit()
    current_app.logger.info(f"[REQ:{g.request_id}] Logout successful")
    return jsonify({"message": "Successfully logged out"}), 200
