"""
Using "Testcontainers for Python" with CrateDB and pytest

Use the `cratedb_service` fixture of cratedb-toolkit, a CrateDB container
bundled with helpers for running SQL and resetting the database.

https://pypi.org/project/cratedb-toolkit/
"""

SQL_STATEMENT = "SELECT mountain FROM sys.summits ORDER BY height DESC LIMIT 3"
HIGHEST_SUMMITS = ["Mont Blanc", "Monte Rosa", "Dom"]


def test_toolkit(cratedb_service):
    rows = cratedb_service.database.run_sql(SQL_STATEMENT)
    assert [row[0] for row in rows] == HIGHEST_SUMMITS
