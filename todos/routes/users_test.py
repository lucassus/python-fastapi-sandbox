from todos.entities import User


def test_user_registration_endpoints(client):
    response = client.post(
        "/users",
        json={"email": "user@email.com", "password": "password"},
    )

    assert response.status_code == 200


def test_user_endpoint(session, client):
    # Given
    user = User(email="test@email.com", password="password")
    session.add(user)
    session.commit()

    # When
    response = client.get(f"/users/{user.id}")
    print(response)

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "test@email.com",
        "password": "password",
    }


def test_user_endpoint_responds_with_404(session, client):
    response = client.get("/users/123")
    assert response.status_code == 404
