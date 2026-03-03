from app.extensions import db


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    token = db.Column(
        db.String(300),
        nullable=False,
        unique=True,
        index=True
    )

    expires_at = db.Column(db.DateTime, nullable=False)

    is_used = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "reset_tokens",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<PasswordResetToken user_id={self.user_id} used={self.is_used}>"