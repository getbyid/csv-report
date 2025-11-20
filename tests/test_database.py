import pytest

from src.database import Database


@pytest.fixture
def db():
    database = Database()
    database.create_schema()
    return database


def test_create_schema(db):
    cursor = db.conn.execute(
        "SELECT name FROM sqlite_schema WHERE type='table' AND name='employees'"
    )
    assert cursor.fetchone() is not None


def test_insert_employee(db):
    data = {"position": "Developer", "performance": 4.6}
    db.insert_employee(data)

    cursor = db.conn.execute("SELECT * FROM employees WHERE position = 'Developer'")

    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "Developer"
    assert row[1] == 4.6


def test_insert_invalid_employee(db):
    with pytest.raises(ValueError):
        db.insert_employee({"position": "Junior", "performance": "---"})


def test_select_performance(db):
    db.insert_employee({"position": "Developer", "performance": 4.6})
    db.insert_employee({"position": "Manager", "performance": 4.9})
    db.insert_employee({"position": "Developer", "performance": 4.8})

    results = db.select_performance()
    assert len(results) == 2
    assert results[0][1] == "Manager"
    assert results[0][2] == pytest.approx(4.9)
    assert results[1][1] == "Developer"
    assert results[1][2] == pytest.approx(4.7)
