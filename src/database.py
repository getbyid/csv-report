import sqlite3


class Database:
    def __init__(self):
        sqlite3.enable_callback_tracebacks(True)
        self.conn = sqlite3.connect(":memory:")

    def create_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                position TEXT NOT NULL,
                performance INTEGER NOT NULL
            )
            """)
        self.conn.commit()

    def insert_employee(self, row):
        self.conn.execute(
            "INSERT INTO employees (position, performance) VALUES (?, ?)",
            (row["position"], float(row["performance"])),
        )

    def select_performance(self):
        return self.conn.execute(
            """
            WITH t AS (
                SELECT
                    position,
                    AVG(performance) AS performance
                FROM employees
                GROUP BY position
                ORDER BY performance DESC
            ) SELECT row_number() over (), * FROM t
            """
        ).fetchall()
