"""
Using "Testcontainers for Python" with CrateDB and pytest

Build test harnesses around CrateDB using the `cratedb_service`
pytest fixture exported by `cratedb-toolkit`.

https://pypi.org/project/cratedb-toolkit/
"""
import subprocess
from pprint import pprint

SQL_STATEMENT = "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3;"


def test_crash(cratedb_service):
    """
    After provisioning a test instance of CrateDB, invoke `crash`.
    """
    http_url = cratedb_service.get_http_url()
    command = f"time crash --hosts '{http_url}' --command '{SQL_STATEMENT}'"
    subprocess.check_call(command, shell=True)


def test_sql(cratedb_service):
    """
    After provisioning a test instance of CrateDB, invoke an SQL statement.
    """
    results = cratedb_service.database.run_sql(SQL_STATEMENT, records=True)
    pprint(results)
