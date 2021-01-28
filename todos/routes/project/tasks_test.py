from datetime import date, datetime

from todos.domain.entities import Project
from todos.routes.dependencies import get_current_time


def test_tasks_endpoint_creates_task(session, client):
    # Given
    project = Project(name="Test project")
    session.add(project)
    session.commit()

    # When
    response = client.post(
        f"/projects/{project.id}/tasks",
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
    project = Project(name="Test project")
    task = project.add_task(name="Test")
    session.add(project)
    session.commit()

    now = datetime(2012, 1, 18, 9, 30)
    client.app.dependency_overrides[get_current_time] = lambda: now

    # When
    response = client.put(f"/projects/{project.id}/tasks/{task.id}/complete")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": task.id,
        "name": task.name,
        "completedAt": "2012-01-18",
    }

    assert task.completed_at == now.date()


# TODO: Is it worth to test it like that?
def test_task_complete_endpoint_returns_404(client):
    response = client.put("/tasks/123/complete")
    assert response.status_code == 404


def test_task_incomplete_endpoint(session, client):
    # Given
    project = Project(name="Test project")
    project.add_task(name="Test")

    task = project.add_task(name="Test")
    task.completed_at = date(2021, 1, 12)

    session.add(project)
    session.commit()

    # When
    response = client.put(f"/projects/{project.id}/tasks/{task.id}/incomplete")

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
    project = Project(name="Project One")
    session.add(project)

    project.add_task(name="Task One")
    task = project.add_task(name="Task Two")
    task.completed_at = date(2021, 1, 6)
    project.add_task(name="Task Three")
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Task One", "completedAt": None},
        {"id": 2, "name": "Task Two", "completedAt": "2021-01-06"},
        {"id": 3, "name": "Task Three", "completedAt": None},
    ]


def test_task_endpoint_returns_task(session, client):
    # Given
    project = Project(name="Project One")
    task = project.add_task(name="Task One")
    session.add(project)
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}/tasks/{task.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Task One", "completedAt": None}


def test_task_endpoint_returns_404(client):
    response = client.get("/projects/123/tasks/123")
    assert response.status_code == 404
