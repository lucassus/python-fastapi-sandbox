import json
from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.tasks import CreateTask, Task


class TestCreateTaskSchema:
    @pytest.mark.parametrize("invalid_name", [None, 123, "", "short"])
    def test_name_validation(self, invalid_name):
        with pytest.raises(ValidationError):
            CreateTask(name=invalid_name)


class TestTaskSchema:
    def test_serialize(self):
        task = Task(id=1, name="Test")

        assert task.dict(by_alias=True) == dict(
            id=1,
            name="Test",
            completedAt=None,
        )

    def test_deserialize(self):
        task = Task.parse_raw(
            json.dumps(
                dict(
                    id=2,
                    name="Test 2",
                    completedAt="2021-01-18",
                )
            )
        )

        assert task
        assert task.id == 2
        assert task.name == "Test 2"
        assert task.completed_at == date(2021, 1, 18)
