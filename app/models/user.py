from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # =====================================================
    # PROFILE
    # =====================================================

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    full_name = db.Column(db.String(200))

    profile_image = db.Column(db.String(500))

    # =====================================================
    # CONTACT
    # =====================================================

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    phone_number = db.Column(db.String(20))

    # =====================================================
    # AUTH
    # =====================================================

    password_hash = db.Column(
        db.String(255),
        nullable=True
    )

    auth_provider = db.Column(
        db.String(50),
        default="local"
    )  # local | google

    google_id = db.Column(
        db.String(200),
        nullable=True,
        index=True
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )  # user | seller | admin

    # =====================================================
    # STATUS
    # =====================================================

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # =====================================================
    # LOGIN TRACKING
    # =====================================================

    last_login_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # =====================================================
    # PASSWORD HELPERS
    # =====================================================

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False

        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
