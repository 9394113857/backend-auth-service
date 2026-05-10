from app.extensions import db


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    ip_address = db.Column(db.String(100))

    user_agent = db.Column(db.String(500))

    device_name = db.Column(db.String(255))

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    last_seen_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
