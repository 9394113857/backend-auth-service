def test_register_user(client):
    res = client.post("/api/v1/auth/angularUser/register", json={
        "email": "user@test.com",
        "password": "12345",
        "role": "user"
    })
    assert res.status_code == 201


def test_login_user(client):
    client.post("/api/v1/auth/angularUser/register", json={
        "email": "login@test.com",
        "password": "12345",
        "role": "user"
    })

    res = client.post("/api/v1/auth/angularUser/login", json={
        "email": "login@test.com",
        "password": "12345"
    })

    assert res.status_code == 200
    assert "access_token" in res.json
