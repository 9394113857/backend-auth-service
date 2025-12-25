from flask import current_app
from werkzeug.security import check_password_hash
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token


# =========================================================
# REGISTER USER / SELLER  ✅ FIXED
# =========================================================
def register_user(email: str, password: str, role: str = "user"):
    # Check existing user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already exists"}, 409

    # ✅ CREATE USER PROPERLY
    user = User(
        email=email,
        role=role
    )

    # ✅ THIS WAS MISSING / WRONG EARLIER
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    current_app.logger.info(
        f"Service: user created id={user.id} email={user.email}"
    )

    return {
        "message": "User registered successfully",
        "role": user.role
    }, 201


# =========================================================
# LOGIN USER / SELLER  ✅ CORRECT
# =========================================================
def authenticate_user(email: str, password: str):
    user = User.query.filter_by(email=email).first()

    if not user:
        current_app.logger.warning(
            f"Service: authenticate_user - user not found email={email}"
        )
        return {"error": "Invalid credentials"}, 401

    # ✅ PASSWORD CHECK (USES MODEL METHOD)
    if not user.check_password(password):
        current_app.logger.warning(
            f"Service: authenticate_user - invalid password for email={email}"
        )
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "role": user.role,
        "userId": user.id
    }, 200
