from app.extensions import db


class UserAddress(db.Model):
    __tablename__ = "user_addresses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    full_name = db.Column(db.String(150))

    phone_number = db.Column(db.String(20))

    address_line_1 = db.Column(db.String(255))

    address_line_2 = db.Column(db.String(255))

    city = db.Column(db.String(100))

    state = db.Column(db.String(100))

    country = db.Column(db.String(100))

    postal_code = db.Column(db.String(20))

    landmark = db.Column(db.String(255))

    is_default = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
