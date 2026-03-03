from flask import current_app
from flask_jwt_extended import create_access_token
from app.models import User
from app.extensions import db


# =========================================================
# REGISTER USER (REQUIRED first_name & last_name)
# =========================================================
def register_user(email: str, password: str, first_name: str, last_name: str):

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already exists"}, 409

    user = User(
        email=email,
        role="user",
        first_name=first_name,
        last_name=last_name
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    current_app.logger.info(
        f"User created id={user.id} email={user.email}"
    )

    return {
        "message": "User registered successfully",
        "role": user.role
    }, 201


# =========================================================
# LOGIN USER
# =========================================================
def authenticate_user(email: str, password: str):

    user = User.query.filter_by(email=email).first()

    if not user or not user.is_active:
        return {"error": "Invalid credentials"}, 401

    if not user.check_password(password):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "role": user.role,
        "userId": user.id
    }, 200