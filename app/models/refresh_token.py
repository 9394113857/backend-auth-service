from app.extensions import db


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    token = db.Column(
        db.String(500),
        nullable=False,
        unique=True
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    is_revoked = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
