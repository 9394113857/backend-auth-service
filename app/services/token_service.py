from datetime import datetime

from app.extensions import db

from app.models import RefreshToken


# =====================================================
# SAVE REFRESH TOKEN
# =====================================================

def save_refresh_token(
    user_id,
    token,
    expires_at
):

    refresh = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.session.add(refresh)

    db.session.commit()

    return refresh


# =====================================================
# REVOKE REFRESH TOKEN
# =====================================================

def revoke_refresh_token(token):

    refresh = RefreshToken.query.filter_by(
        token=token
    ).first()

    if refresh:
        refresh.is_revoked = True

        db.session.commit()

    return refresh
