from todos.infrastructure.tables import users_table
from todos.models import User


def test_user_registration_endpoints(session, client):
    response = client.post(
        "/users",
        json={"email": "user@email.com", "password": "password"},
    )

    assert response.status_code == 200

    user: User = session.query(User).order_by(users_table.c.id.desc()).first()
    assert response.json() == {
        "id": user.id,
        "email": user.email,
        "password": user.password,
        "projects": [
            {"id": 1, "name": "My first project"},
        ],
    }


def test_user_endpoint(session, client):
    # Given
    user = User(email="user@email.com", password="password")
    session.add(user)
    session.commit()

    # When
    response = client.get(f"/users/{user.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "user@email.com",
        "password": "password",
        "projects": [],
    }


def test_user_endpoint_responds_with_404(session, client):
    response = client.get("/users/123")
    assert response.status_code == 404
    assert response.json() == {"detail": "Unable to find a user with id=123"}
