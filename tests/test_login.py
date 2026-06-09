from tests.conftest import login


def test_valid_user_can_login(client):
    response = login(client)

    assert response.status_code == 200
    assert b"Login successful" in response.data
    assert b"Support Tickets" in response.data


def test_invalid_login_fails_safely(client):
    response = login(
        client,
        email="user@test.com",
        password="WrongPassword123!"
    )

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data
    assert b"Support Tickets" not in response.data