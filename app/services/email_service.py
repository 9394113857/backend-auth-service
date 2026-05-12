# =====================================================
# EMAIL SERVICE
# =====================================================

from flask import current_app

from flask_mail import Message

from app.extensions import mail


# =====================================================
# EMAIL VERIFICATION
# =====================================================

def send_verification_email(
    email,
    token
):

    # =====================================================
    # DIRECT BACKEND VERIFY URL
    # =====================================================

    verify_link = (
        f"http://127.0.0.1:5000"
        f"/api/v1/auth/angularUser/verify-email/{token}"
    )

    msg = Message(
        subject="Verify Your Email",
        recipients=[email],
        sender=current_app.config["MAIL_USERNAME"]
    )

    msg.html = f"""
    <h2>Welcome to Our Platform</h2>

    <p>Thank you for registering.</p>

    <p>Please verify your email below:</p>

    <a href="{verify_link}"
       style="
            padding:10px 20px;
            background:#4CAF50;
            color:white;
            text-decoration:none;
            border-radius:5px;
       ">
       Verify Email
    </a>
    """

    mail.send(msg)


# =====================================================
# PASSWORD RESET EMAIL
# =====================================================

def send_reset_email(
    email,
    token
):

    # =====================================================
    # DIRECT BACKEND RESET URL
    # =====================================================

    reset_link = (
        f"http://127.0.0.1:5000"
        f"/api/v1/auth/reset-password/{token}"
    )

    msg = Message(
        subject="Password Reset Request",
        recipients=[email],
        sender=current_app.config["MAIL_USERNAME"]
    )

    msg.html = f"""
    <h2>Password Reset</h2>

    <p>You requested a password reset.</p>

    <a href="{reset_link}"
       style="
            padding:10px 20px;
            background:#ff6600;
            color:white;
            text-decoration:none;
            border-radius:5px;
       ">
       Reset Password
    </a>
    """

    mail.send(msg)