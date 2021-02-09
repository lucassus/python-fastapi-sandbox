from datetime import date, datetime

from app.factories import build_user
from app.routes.dependencies import get_current_time


def test_tasks_endpoint_creates_task(session, client):
    # Given
    user = build_user()
    session.add(user)
    session.commit()

    # When
    response = client.post(
        f"/users/{user.id}/tasks",
        json={"name": "Some task"},
    )

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Some task",
        "completedAt": None,
    }


def test_task_complete_endpoint(session, client):
    # Given
    user = build_user()
    task = user.add_task(name="Test")
    session.add(user)
    session.commit()

    now = datetime(2012, 1, 18, 9, 30)
    client.app.dependency_overrides[get_current_time] = lambda: now

    # When
    response = client.put(f"/users/{user.id}/tasks/{task.id}/complete")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": task.id,
        "name": task.name,
        "completedAt": "2012-01-18",
    }

    assert task.completed_at == now.date()


def test_task_complete_endpoint_returns_404(client):
    response = client.put("/tasks/123/complete")
    assert response.status_code == 404


def test_task_incomplete_endpoint(session, client):
    # Given
    user = build_user()
    user.add_task(name="Test")

    task = user.add_task(name="Test")
    task.completed_at = date(2021, 1, 12)

    session.add(user)
    session.commit()

    # When
    response = client.put(f"/users/{user.id}/tasks/{task.id}/incomplete")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": task.id,
        "name": task.name,
        "completedAt": None,
    }


def test_task_incomplete_endpoint_returns_404(client):
    response = client.put("/tasks/123/incomplete")
    assert response.status_code == 404


def test_tasks_endpoint(session, client):
    # Given
    user = build_user()
    session.add(user)

    user.add_task(name="Task One")
    task = user.add_task(name="Task Two")
    task.completed_at = date(2021, 1, 6)
    user.add_task(name="Task Three")
    session.commit()

    # When
    response = client.get(f"/users/{user.id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Task One", "completedAt": None},
        {"id": 2, "name": "Task Two", "completedAt": "2021-01-06"},
        {"id": 3, "name": "Task Three", "completedAt": None},
    ]


def test_task_endpoint_returns_404_when_task_not_found(session, client):
    # Given
    user = build_user()
    session.add(user)
    session.commit()

    # When
    response = client.get(f"/users/{user.id}/tasks/123")

    # Then
    assert response.status_code == 404
    assert response.json() == {"detail": "Unable to find a task with id=123"}


def test_task_endpoint_returns_task(session, client):
    # Given
    user = build_user()
    task = user.add_task(name="Task One")
    session.add(user)
    session.commit()

    # When
    response = client.get(f"/users/{user.id}/tasks/{task.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Task One", "completedAt": None}


def test_task_endpoint_returns_404_when_user_not_found(session, client):
    # Given
    user = build_user()
    task = user.add_task(name="Test task")
    session.add(user)
    session.commit()

    # When
    response = client.get(f"/users/123/tasks/{task.id}")

    # Then
    assert response.status_code == 404
    assert response.json() == {"detail": "Unable to find a user with id=123"}
