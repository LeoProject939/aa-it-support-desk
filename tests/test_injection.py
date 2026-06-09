from tests.conftest import login


def test_sql_injection_payload_does_not_bypass_login(client):
    response = login(
        client,
        email="' OR '1'='1",
        password="' OR '1'='1"
    )

    assert response.status_code == 200
    assert (
        b"Invalid email or password" in response.data
        or b"Enter a valid email address" in response.data
    )
    assert b"Support Tickets" not in response.data


def test_sql_injection_payload_in_ticket_title_is_handled_as_text(client):
    login(client)

    response = client.post(
        "/tickets/new",
        data={
            "title": "' OR '1'='1 test",
            "description": "Testing that SQL-like input is stored as text safely.",
            "priority": "Medium",
            "category_id": 1
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Ticket created successfully" in response.data
    assert b"&#39; OR &#39;1&#39;=&#39;1 test" in response.data or b"OR" in response.data