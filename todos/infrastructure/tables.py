from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, String

from todos.entities import Project, Task, User

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255)),
    Column("password", String(255)),
)

projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("name", String(255)),
    Column("max_incomplete_tasks_number", Integer),
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("name", String(255)),
    Column("completed_at", Date, nullable=True),
)


def create_tables(engine):
    metadata.create_all(bind=engine)


def drop_tables(engine):
    metadata.drop_all(bind=engine)


def start_mappers():
    mapper(User, users_table)

    mapper(
        Project,
        projects_table,
        properties={
            "tasks": relationship(Task, order_by=tasks_table.c.id),
        },
    )

    mapper(Task, tasks_table)
