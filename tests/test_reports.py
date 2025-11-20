from pathlib import Path
from unittest.mock import patch

import pytest

from src.database import Database
from src.reports import PerformanceReport


@pytest.fixture
def csv_file(tmp_path: Path):
    p = tmp_path / "employees.csv"
    p.write_text(
        "name,position,completed_tasks,performance\n"
        "Alex Ivanov,Backend Developer,45,4.8\n"
        "Maria Petrova,Frontend Developer,38,4.7\n"
        "Tom Anderson,Backend Developer,49,4.9\n"
    )

    yield str(p)


def test_add_employees(csv_file):
    report = PerformanceReport()
    report.add_employees(csv_file)

    result = report.make()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0][1] == "Backend Developer"
    assert result[0][2] == 4.85


def test_performance_report_properties():
    report = PerformanceReport()
    assert report.report_type == "performance"
    assert report.headers == ("", "position", "performance")


@patch.object(Database, "select_performance", return_value=[(1, "Developer", 4.5)])
def test_performance_report_make(mock_select):
    report = PerformanceReport()

    result = report.make()
    assert mock_select.call_count == 1
    assert result == [(1, "Developer", 4.5)]
