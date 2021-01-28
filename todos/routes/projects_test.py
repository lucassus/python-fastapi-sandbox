from todos.entities import Project


def test_projects_endpoint_returns_list_of_projects(session, client):
    # Given
    session.add(Project(name="Project One"))
    session.add(Project(name="Project Two"))
    session.commit()

    # When
    response = client.get("/projects")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Project One"},
        {"id": 2, "name": "Project Two"},
    ]


def test_project_endpoint_returns_the_project(session, client):
    # Given
    project = Project(name="Project One")
    session.add(project)
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Project One"}


def test_project_endpoint_responds_with_404_if_project_cannot_be_found(client):
    response = client.get("/projects/123")
    assert response.status_code == 404
