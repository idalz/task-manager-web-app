def test_register_user(client):
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    response = client.post("/users/register/", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data # make sure we don't expose password
    