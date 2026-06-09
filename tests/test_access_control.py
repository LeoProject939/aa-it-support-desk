from tests.conftest import login


def test_protected_ticket_page_redirects_when_not_logged_in(client):
    response = client.get("/tickets/", follow_redirects=True)

    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    assert b"Login" in response.data


def test_regular_user_blocked_from_admin_dashboard(client):
    login(client)

    response = client.get("/admin/")

    assert response.status_code == 403
    assert b"Access denied" in response.data


def test_admin_can_access_admin_dashboard(client):
    login(client, email="admin@test.com", password="AdminPass123!")

    response = client.get("/admin/")

    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data