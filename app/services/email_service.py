# ===============================================================
# EMAIL SERVICE
# ===============================================================
# This service handles sending emails from the backend.
#
# Emails Supported:
#   1. Email Verification (during signup)
#   2. Password Reset (forgot password flow)
#
# Production Debugging:
#   Railway sometimes hides logging inside files,
#   so we print important logs to STDOUT as well.
#
# This ensures Railway Deployment Logs show email errors.
# ===============================================================

from flask_mail import Message
from flask import current_app
from app.extensions import mail


# ===============================================================
# SEND VERIFICATION EMAIL
# ===============================================================
# Called when user registers
#
# Steps:
#   1. Build verification link
#   2. Create email message
#   3. Send email using Flask-Mail
#   4. Log success or error
# ===============================================================
def send_verification_email(email, token):

    # -----------------------------------------------------------
    # Construct verification link
    # Example:
    # https://angular-app.com/verify-email?token=abc123
    # -----------------------------------------------------------
    verify_link = f"{current_app.config['FRONTEND_URL']}/verify-email?token={token}"

    # -----------------------------------------------------------
    # Create email message
    # -----------------------------------------------------------
    msg = Message(
        subject="Verify Your Email",
        recipients=[email],
        sender=current_app.config["MAIL_USERNAME"]
    )

    # -----------------------------------------------------------
    # Email HTML content
    # -----------------------------------------------------------
    msg.html = f"""
    <h2>Welcome to Our Platform</h2>

    <p>Thank you for registering.</p>

    <p>Please verify your email by clicking the button below:</p>

    <a href="{verify_link}"
       style="
            padding:12px 25px;
            background:#4CAF50;
            color:white;
            text-decoration:none;
            border-radius:6px;
            font-weight:bold;">
       Verify Email
    </a>

    <p>If you did not create this account, please ignore this email.</p>
    """

    # -----------------------------------------------------------
    # Send Email
    # -----------------------------------------------------------
    try:

        # Attempt to send email
        mail.send(msg)

        # Railway logs visibility
        print(f"EMAIL SENT SUCCESSFULLY → {email}")

        # Application log
        current_app.logger.info(
            f"Verification email sent to {email}"
        )

    except Exception as e:

        # Print to Railway console logs
        print("EMAIL ERROR:", str(e))

        # Save in application logs
        current_app.logger.error(
            f"Verification email FAILED for {email}: {str(e)}"
        )


# ===============================================================
# SEND PASSWORD RESET EMAIL
# ===============================================================
# Called when user clicks "Forgot Password"
#
# Steps:
#   1. Generate reset link
#   2. Build email
#   3. Send email
#   4. Log success or error
# ===============================================================
def send_reset_email(email, token):

    # -----------------------------------------------------------
    # Construct reset password link
    # Example:
    # https://angular-app.com/reset-password?token=abc123
    # -----------------------------------------------------------
    reset_link = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"

    # -----------------------------------------------------------
    # Create email message
    # -----------------------------------------------------------
    msg = Message(
        subject="Password Reset Request",
        recipients=[email],
        sender=current_app.config["MAIL_USERNAME"]
    )

    # -----------------------------------------------------------
    # Email HTML template
    # -----------------------------------------------------------
    msg.html = f"""
    <h2>Password Reset Request</h2>

    <p>You requested to reset your password.</p>

    <a href="{reset_link}"
       style="
            padding:12px 25px;
            background:#ff6600;
            color:white;
            text-decoration:none;
            border-radius:6px;
            font-weight:bold;">
       Reset Password
    </a>

    <p>If you did not request this reset, please ignore this email.</p>
    """

    # -----------------------------------------------------------
    # Send email
    # -----------------------------------------------------------
    try:

        mail.send(msg)

        # Railway visible log
        print(f"RESET EMAIL SENT → {email}")

        current_app.logger.info(
            f"Password reset email sent to {email}"
        )

    except Exception as e:

        # Railway visible error
        print("RESET EMAIL ERROR:", str(e))

        current_app.logger.error(
            f"Password reset email FAILED for {email}: {str(e)}"
        )