# ===============================================================
# EMAIL SERVICE
# Handles:
# - Email verification
# - Password reset
# Includes logging for Railway debugging
# ===============================================================

from flask_mail import Message
from flask import current_app
from app.extensions import mail


# ===============================================================
# SEND VERIFICATION EMAIL
# ===============================================================
def send_verification_email(email, token):

    verify_link = f"{current_app.config['FRONTEND_URL']}/verify-email?token={token}"

    msg = Message(
        subject="Verify Your Email",
        recipients=[email],
        sender=current_app.config["MAIL_USERNAME"]
    )

    msg.html = f"""
    <h2>Welcome to Our Platform</h2>

    <p>Thank you for registering.</p>

    <p>Please verify your email by clicking the button below:</p>

    <a href="{verify_link}" 
       style="padding:10px 20px;
              background:#4CAF50;
              color:white;
              text-decoration:none;
              border-radius:5px;">
       Verify Email
    </a>

    <p>If you did not create this account, please ignore this email.</p>
    """

    try:
        mail.send(msg)
        current_app.logger.info(f"Verification email sent to {email}")

    except Exception as e:
        current_app.logger.error(f"Verification email FAILED for {email}: {str(e)}")


# ===============================================================
# SEND PASSWORD RESET EMAIL
# ===============================================================
def send_reset_email(email, token):

    reset_link = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"

    msg = Message(
        subject="Password Reset Request",
        recipients=[email],
        sender=current_app.config["MAIL_USERNAME"]
    )

    msg.html = f"""
    <h2>Password Reset</h2>

    <p>You requested a password reset.</p>

    <a href="{reset_link}"
       style="padding:10px 20px;
              background:#ff6600;
              color:white;
              text-decoration:none;
              border-radius:5px;">
       Reset Password
    </a>

    <p>If you did not request this, please ignore this email.</p>
    """

    try:
        mail.send(msg)
        current_app.logger.info(f"Password reset email sent to {email}")

    except Exception as e:
        current_app.logger.error(f"Password reset email FAILED for {email}: {str(e)}")