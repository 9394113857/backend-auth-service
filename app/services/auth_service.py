from ..models.user import User
from ..extensions import db
from flask import current_app


def register_user(email, password):
    """
    Create and save a new user.
    Returns: (response_dict, status_code)
    """
    current_app.logger.debug(f"Service: register_user called for email={email}")

    if User.query.filter_by(email=email).first():
        current_app.logger.warning(f"Service: register_user - email exists: {email}")
        return {"message": "Email already exists"}, 400

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    current_app.logger.info(f"Service: user created id={user.id} email={email}")
    return {"message": "User registered successfully"}, 201


def authenticate_user(email, password):
    """
    Return user object on valid credentials, otherwise None.
    """
    current_app.logger.debug(f"Service: authenticate_user called for email={email}")

    user = User.query.filter_by(email=email).first()
    if not user:
        current_app.logger.warning(f"Service: authenticate_user - no user found for email={email}")
        return None

    if not user.check_password(password):
        current_app.logger.warning(f"Service: authenticate_user - invalid password for email={email}")
        return None

    current_app.logger.debug(f"Service: authenticate_user - success user_id={user.id}")
    return user
