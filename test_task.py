import pytest
from task import (
    load_database,
    add_task,
    update_task,
    delete_task,
)

DATABASE_PATH = "test.json"
database = load_database(DATABASE_PATH)

def test_add_task():
    # add single task
    add_task(database, "test1")
    assert len(database) == 1 and database["1"]["description"] == "test1"

    # add multiple tasks
    add_task(database, "do leetcode")
    add_task(database, "wash clothes")
    add_task(database, "get an internship :(")
    assert len(database) == 4 and database["4"]["description"] == "get an internship :("

def test_update_task():
    # update single task
    update_task(database, "1", "go to gym")
    assert database["1"]["description"] == "go to gym"

    # update others, check that date gets updated
    update_task(database, "3", "meal prep")
    assert database["3"]["description"] == "meal prep" and database["3"]["createdAt"] != database["3"]["updatedAt"]

    # update invalid/non-existent id
    with pytest.raises(KeyError):
        update_task(database, "100", "this wont work")
    with pytest.raises(KeyError):
        update_task(database, 1, "this wont work")

def test_delete_task():
    # delete tasks
    delete_task(database, "1")
    assert len(database) == 3 and "1" not in database
    delete_task(database, "3")
    assert len(database) == 2 and "3" not in database

    # delete non-existent task
    with pytest.raises(KeyError):
        delete_task(database, "3")
    with pytest.raises(KeyError):
        delete_task(database, "99")