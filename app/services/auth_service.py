from flask import current_app
from flask_jwt_extended import create_access_token
from app.models import User, PasswordHistory, EmailVerificationToken
from app.extensions import db
from app.services.email_service import send_verification_email

import secrets
from datetime import datetime, timedelta


# =========================================================
# REGISTER USER
# =========================================================
def register_user(email: str, password: str, first_name: str, last_name: str):

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already exists"}, 409

    user = User(
        email=email,
        role="user",
        first_name=first_name,
        last_name=last_name,
        is_verified=False
    )

    user.set_password(password)

    db.session.add(user)
    db.session.flush()

    # Save password history
    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    db.session.add(history)

    # ------------------------------------------------
    # CREATE EMAIL VERIFICATION TOKEN
    # ------------------------------------------------
    token = secrets.token_urlsafe(48)

    verification = EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.session.add(verification)

    db.session.commit()

    # ------------------------------------------------
    # SEND VERIFICATION EMAIL
    # ------------------------------------------------
    send_verification_email(user.email, token)

    current_app.logger.info(
        f"User created id={user.id} email={user.email}"
    )

    return {
        "message": "Registration successful. Please verify your email."
    }, 201


# =========================================================
# LOGIN USER
# =========================================================
def authenticate_user(email: str, password: str):

    user = User.query.filter_by(email=email).first()

    if not user or not user.is_active:
        return {"error": "Invalid credentials"}, 401

    # ------------------------------------------------
    # CHECK EMAIL VERIFIED
    # ------------------------------------------------
    if not user.is_verified:
        return {"error": "Please verify your email before login"}, 403

    # ------------------------------------------------
    # CHECK PASSWORD
    # ------------------------------------------------
    if not user.check_password(password):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "role": user.role,
        "userId": user.id
    }, 200