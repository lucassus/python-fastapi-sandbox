from todos.test_utils.factories import build_user


def test_add_task():
    user = build_user()
    assert len(user.tasks) == 0

    task = user.add_task(name="Testing")

    assert len(user.tasks) == 1
    assert user.tasks == [task]
