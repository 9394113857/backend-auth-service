from flask_jwt_extended import decode_token

from app.extensions import db
from app.models.user import User


def test_public_registration_cannot_assign_admin_role(client):
    response = client.post(
        "/api/v1/auth/angularUser/register",
        json={"email": "attacker@example.com", "password": "StrongPass123!", "role": "admin"},
    )
    assert response.status_code == 403
    assert User.query.filter_by(email="attacker@example.com").first() is None


def test_login_access_token_contains_database_role(client, app):
    with app.app_context():
        user = User(email="reviewer@example.com", role="admin")
        user.set_password("StrongPass123!")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/api/v1/auth/angularUser/login",
        json={"email": "reviewer@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 200
    assert response.get_json()["role"] == "admin"

    with app.app_context():
        claims = decode_token(response.get_json()["access_token"])
        assert claims["role"] == "admin"


def test_refresh_access_token_keeps_database_role(client, app):
    with app.app_context():
        user = User(email="refresh-reviewer@example.com", role="admin")
        user.set_password("StrongPass123!")
        db.session.add(user)
        db.session.commit()

    login = client.post(
        "/api/v1/auth/angularUser/login",
        json={"email": "refresh-reviewer@example.com", "password": "StrongPass123!"},
    )
    refresh_token = login.get_json()["refresh_token"]
    refreshed = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert refreshed.status_code == 200

    with app.app_context():
        claims = decode_token(refreshed.get_json()["access_token"])
        assert claims["role"] == "admin"
