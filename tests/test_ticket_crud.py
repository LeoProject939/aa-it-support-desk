from tests.conftest import login


def test_logged_in_user_can_view_ticket_list(client):
    login(client)

    response = client.get("/tickets/")

    assert response.status_code == 200
    assert b"Support Tickets" in response.data
    assert b"VPN connection issue" in response.data


def test_user_can_create_ticket(client):
    login(client)

    response = client.post(
        "/tickets/new",
        data={
            "title": "Laptop screen issue",
            "description": "The laptop screen flickers when opening applications.",
            "priority": "Medium",
            "category_id": 1
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Ticket created successfully" in response.data
    assert b"Laptop screen issue" in response.data


def test_ticket_validation_rejects_short_title(client):
    login(client)

    response = client.post(
        "/tickets/new",
        data={
            "title": "Bad",
            "description": "This description is long enough for validation.",
            "priority": "Medium",
            "category_id": 1
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Field must be between 5 and 120 characters long" in response.data