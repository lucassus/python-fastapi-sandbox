from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, String

from app.models import Task, User

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255)),
    Column("password", String(255)),
)

tasks_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey(users_table.c.id)),
    Column("name", String(255)),
    Column("completed_at", Date, nullable=True),
)


def create_tables(engine):
    metadata.create_all(bind=engine)


def drop_tables(engine):
    metadata.drop_all(bind=engine)


def start_mappers():
    mapper(
        User,
        users_table,
        properties={"tasks": relationship(Task, order_by=tasks_table.c.id)},
    )

    mapper(Task, tasks_table)
