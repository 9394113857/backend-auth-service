# =====================================================
# EMAIL SERVICE
# =====================================================

from flask import current_app

import resend


# =====================================================
# FRONTEND URL
# =====================================================

# FRONTEND_URL = "http://localhost:4200"

FRONTEND_URL = (
    "https://scintillating-cheesecake-39e8db.netlify.app"
)


# =====================================================
# EMAIL VERIFICATION
# =====================================================

def send_verification_email(
    email,
    token
):

    # =====================================================
    # RESEND API KEY
    # =====================================================

    resend.api_key = current_app.config[
        "RESEND_API_KEY"
    ]

    # =====================================================
    # ANGULAR VERIFY URL
    # =====================================================

    verify_link = (
        f"{FRONTEND_URL}"
        f"/verify-email/{token}"
    )

    resend.Emails.send({

        # =================================================
        # TEST EMAIL (SANDBOX)
        # =================================================

        "from": "practicesession3@gmail.com",

        "to": email,

        "subject": "Verify Your Email",

        "html": f"""

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

    })


# =====================================================
# PASSWORD RESET EMAIL
# =====================================================

def send_reset_email(
    email,
    token
):

    # =====================================================
    # RESEND API KEY
    # =====================================================

    resend.api_key = current_app.config[
        "RESEND_API_KEY"
    ]

    # =====================================================
    # ANGULAR RESET URL
    # =====================================================

    reset_link = (
        f"{FRONTEND_URL}"
        f"/reset-password/{token}"
    )

    resend.Emails.send({

        # =================================================
        # TEST EMAIL (SANDBOX)
        # =================================================

        "from": "onboarding@resend.dev",

        "to": email,

        "subject": "Password Reset Request",

        "html": f"""

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

    })