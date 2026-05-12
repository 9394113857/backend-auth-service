# =====================================================
# AUTH SERVICE
# =====================================================

from datetime import datetime, timedelta

import secrets

from flask import current_app

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from app.extensions import db

from app.models import (
    User,
    PasswordHistory,
    EmailVerificationToken
)

from app.services.email_service import (
    send_verification_email
)

from app.services.token_service import (
    save_refresh_token
)


# =====================================================
# REGISTER USER
# =====================================================

def register_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: str = "user"
):

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return {
            "error": "Email already exists"
        }, 409

    # =====================================================
    # ROLE VALIDATION
    # =====================================================

    if role not in ["user", "seller"]:
        role = "user"

    # =====================================================
    # USER
    # =====================================================

    user = User(
        email=email,
        role=role,
        first_name=first_name,
        last_name=last_name,
        full_name=(
            f"{first_name or ''} "
            f"{last_name or ''}"
        ).strip(),
        is_verified=False
    )

    user.set_password(password)

    db.session.add(user)

    db.session.flush()

    # =====================================================
    # PASSWORD HISTORY
    # =====================================================

    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    db.session.add(history)

    # =====================================================
    # EMAIL VERIFICATION TOKEN
    # =====================================================

    token = secrets.token_urlsafe(48)

    verification = EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.session.add(verification)

    db.session.commit()

    # =====================================================
    # SEND EMAIL
    # =====================================================

    send_verification_email(
        user.email,
        token
    )

    current_app.logger.info(
        f"User created id={user.id} "
        f"email={user.email} "
        f"role={user.role}"
    )

    return {
        "message": "Registration successful. Please verify your email."
    }, 201


# =====================================================
# LOGIN USER
# =====================================================

def authenticate_user(
    email: str,
    password: str
):

    user = User.query.filter_by(
        email=email
    ).first()

    if not user or not user.is_active:
        return {
            "error": "Invalid credentials"
        }, 401

    # =====================================================
    # EMAIL VERIFIED
    # =====================================================

    if not user.is_verified:
        return {
            "error": "Please verify your email before login"
        }, 403

    # =====================================================
    # PASSWORD CHECK
    # =====================================================

    if not user.check_password(password):
        return {
            "error": "Invalid credentials"
        }, 401

    # =====================================================
    # LOGIN TRACKING
    # =====================================================

    user.last_login_at = datetime.utcnow()

    db.session.commit()

    # =====================================================
    # TOKENS
    # =====================================================

    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    # =====================================================
    # SAVE REFRESH TOKEN
    # =====================================================

    save_refresh_token(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role,
        "userId": user.id
    }, 200