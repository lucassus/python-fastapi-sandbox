import pytest

from todos.entities import Project
from todos.infrastructure.tables import projects_table


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


@pytest.mark.asyncio
async def test_project_endpoint_returns_the_project(database, client):
    # Given
    await database.execute(
        query=projects_table.insert(),
        values={"name": "Project One"},
    )

    # When
    response = await client.get("/projects/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Project One"}


@pytest.mark.asyncio
async def test_project_endpoint_responds_with_404_if_project_cannot_be_found(client):
    response = await client.get("/projects/1")
    assert response.status_code == 404
