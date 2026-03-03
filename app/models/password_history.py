from ..extensions import db


class PasswordHistory(db.Model):
    __tablename__ = "password_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "password_history",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<PasswordHistory user_id={self.user_id}>"