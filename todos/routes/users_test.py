from todos.entities import User


def test_user_endpoint(session, client):
    # Given
    user = User(email="test@email.com", password="password")
    session.add(user)
    session.commit()

    # When
    response = client.get(f"/users/{user.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "test@email.com",
        "password": "password"
    }


def test_user_endpoint_responds_with_404(session, client):
    response = client.get("/users/123")
    assert response.status_code == 404
