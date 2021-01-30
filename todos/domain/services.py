from datetime import date

from todos.domain.entities import Project, User


# TODO: It's not a service!
def build_user_with_example_project(*, email: str, password: str, now: date) -> User:
    user = User(email=email, password=password)

    project = Project(name="My first project")
    user.projects.append(project)

    task = project.add_task(name="Sign up!")
    task.completed_at = now

    project.add_task(name="Watch the tutorial")
    project.add_task(name="Start using our awesome app")

    return user
