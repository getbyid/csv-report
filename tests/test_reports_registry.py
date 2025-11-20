from src.reports import BaseReport, ReportsRegistry


class AnotherReport(BaseReport):
    report_type = "another"

    @property
    def headers(self):
        return ("key", "value")

    def make(self):
        return [("a", 1), ("b", 2)]


def test_performance_report():
    report = ReportsRegistry.get("performance")
    assert isinstance(report, BaseReport)


def test_unknown_report():
    report = ReportsRegistry.get("---")
    assert report is None


def test_another_report():
    report = ReportsRegistry.get("another")
    assert isinstance(report, AnotherReport)

    result = report.make()
    assert len(result) == 2
    assert result[0][0] == "a"
    assert result[0][1] == 1
