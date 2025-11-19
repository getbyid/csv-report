import argparse
import sys

from tabulate import tabulate

from src.reports import ReportsRegistry


def main():
    parser = argparse.ArgumentParser(description="Employees performance analysis")
    parser.add_argument(
        "--files",
        nargs="+",
        help="input csv files",
    )
    parser.add_argument(
        "--report",
        choices=ReportsRegistry.keys(),
        default="performance",
        help="report type",
    )

    args = parser.parse_args()

    report = ReportsRegistry.get(args.report)
    if not report:
        print("Report not found")
        return 1

    for file in args.files:
        try:
            report.add_employees(file)
        except FileNotFoundError:
            print("File not found: ", file)
            return 2
        except KeyError:
            print("Invalid file format: ", file)
            return 3

    table = report.make()
    print(tabulate(table, headers=report.headers, floatfmt=".2f"))


if __name__ == "__main__":
    sys.exit(main())
