def test_homepage_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Internal AA IT Support Desk" in response.data