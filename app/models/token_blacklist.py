from app.extensions import db


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)

    jti = db.Column(
        db.String(200),
        nullable=False,
        unique=True,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<TokenBlocklist jti={self.jti}>"