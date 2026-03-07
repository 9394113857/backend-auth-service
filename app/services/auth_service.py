# =========================================================
# AUTH SERVICE
# =========================================================
# Handles:
#   - User Registration
#   - Email Verification Token creation
#   - Password history tracking
#   - Login Authentication
#
# This service layer is used by auth_routes.py
# =========================================================

from flask import current_app
from flask_jwt_extended import create_access_token

from app.models import (
    User,
    PasswordHistory,
    EmailVerificationToken
)

from app.extensions import db
from app.services.email_service import send_verification_email

import secrets
from datetime import datetime, timedelta


# =========================================================
# REGISTER USER
# =========================================================
# Flow:
#   1. Check if email already exists
#   2. Create new user
#   3. Save password history
#   4. Generate verification token
#   5. Save verification token
#   6. Commit transaction
#   7. Send verification email
# =========================================================
def register_user(email, password, first_name, last_name, role):

    # -----------------------------------------------------
    # Check existing user
    # -----------------------------------------------------
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "Email already exists"}, 409

    # -----------------------------------------------------
    # Create new user
    # -----------------------------------------------------
    user = User(
        email=email,
        role=role,
        first_name=first_name,
        last_name=last_name,
        is_verified=False
    )

    # Hash password
    user.set_password(password)

    db.session.add(user)

    # Flush to generate user.id before commit
    db.session.flush()

    current_app.logger.info(
        f"Service: user created id={user.id} email={email}"
    )

    # -----------------------------------------------------
    # Store password history
    # -----------------------------------------------------
    history = PasswordHistory(
        user_id=user.id,
        password_hash=user.password_hash
    )

    db.session.add(history)

    # -----------------------------------------------------
    # Generate verification token
    # -----------------------------------------------------
    token = secrets.token_urlsafe(48)

    verification = EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.session.add(verification)

    # -----------------------------------------------------
    # Commit DB transaction
    # -----------------------------------------------------
    db.session.commit()

    current_app.logger.info(
        f"Verification token created for user={email}"
    )

    # -----------------------------------------------------
    # Send verification email
    # -----------------------------------------------------
    try:

        send_verification_email(user.email, token)

        current_app.logger.info(
            f"Verification email triggered for {email}"
        )

    except Exception as e:

        # Important for Railway debugging
        print("EMAIL ERROR:", str(e))

        current_app.logger.error(
            f"Email sending failed for {email}: {str(e)}"
        )

    return {
        "message": "Registration successful. Please verify your email."
    }, 201


# =========================================================
# LOGIN USER
# =========================================================
# Flow:
#   1. Find user
#   2. Check active status
#   3. Check email verified
#   4. Verify password
#   5. Issue JWT token
# =========================================================
def authenticate_user(email, password):

    user = User.query.filter_by(email=email).first()

    # -----------------------------------------------------
    # User not found or inactive
    # -----------------------------------------------------
    if not user or not user.is_active:

        current_app.logger.warning(
            f"Service: authenticate_user - invalid credentials email={email}"
        )

        return {"error": "Invalid credentials"}, 401

    # -----------------------------------------------------
    # Email not verified
    # -----------------------------------------------------
    if not user.is_verified:
        return {"error": "Please verify your email before login"}, 403

    # -----------------------------------------------------
    # Password mismatch
    # -----------------------------------------------------
    if not user.check_password(password):

        current_app.logger.warning(
            f"Service: authenticate_user - wrong password email={email}"
        )

        return {"error": "Invalid credentials"}, 401

    # -----------------------------------------------------
    # Generate JWT
    # -----------------------------------------------------
    access_token = create_access_token(identity=str(user.id))

    current_app.logger.info(
        f"User logged in successfully id={user.id}"
    )

    return {
        "access_token": access_token,
        "role": user.role,
        "userId": user.id
    }, 200