# =========================================================
# AUTH SERVICE
# =========================================================
# Handles:
#   - User Registration
#   - Email Verification Token creation
#   - Password history tracking
#   - Login Authentication
#
# IMPORTANT FIX
# Email sending is executed in a background thread so the
# request does not block and cause Gunicorn worker timeout.
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
import threading
from datetime import datetime, timedelta


# =========================================================
# REGISTER USER
# =========================================================
def register_user(email, password, first_name, last_name, role):

    # -----------------------------------------------------
    # Check if email already exists
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

    # Generate user.id before commit
    db.session.flush()

    current_app.logger.info(
        f"Service: user created id={user.id} email={email}"
    )


    # -----------------------------------------------------
    # Save password history
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
    # Commit database transaction
    # -----------------------------------------------------
    db.session.commit()

    current_app.logger.info(
        f"Verification token created for user={email}"
    )


    # =====================================================
    # SEND EMAIL IN BACKGROUND THREAD
    # =====================================================
    try:

        def send_email_background(app, email, token):
            """
            Run email sending in a background thread with
            Flask application context.
            """
            with app.app_context():
                send_verification_email(email, token)

        thread = threading.Thread(
            target=send_email_background,
            args=(current_app._get_current_object(), user.email, token),
            daemon=True
        )

        thread.start()

        current_app.logger.info(
            f"Verification email triggered asynchronously for {email}"
        )

    except Exception as e:

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
    # Generate JWT token
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