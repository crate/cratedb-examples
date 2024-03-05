"""
Using "pytest-crate" with CrateDB and pytest

Build test harnesses around CrateDB using the `crate` pytest fixture
exported by `pytest-crate`. In turn, this is using `CrateNode`
exported by `cr8`.

https://pypi.org/project/pytest-crate/
https://pypi.org/project/cr8/
"""
import subprocess

SQL_STATEMENT = "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3;"


def test_crash(crate):
    """
    After provisioning a test instance of CrateDB, invoke `crash`.
    """
    http_url = crate.dsn()
    command = f"time crash --hosts '{http_url}' --command 'SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3;'"
    subprocess.check_call(command, shell=True)


def test_crate(crate):
    assert crate.dsn().startswith("http://127.0.0.1:42")
    assert "http" in crate.addresses
    assert crate.addresses["http"].host == "127.0.0.1"
    assert 4300 > crate.addresses["http"].port >= 4200
    assert "psql" in crate.addresses
    assert crate.addresses["psql"].host == "127.0.0.1"
    assert 5500 > crate.addresses["psql"].port >= 5432
    assert "transport" in crate.addresses
    assert crate.addresses["transport"].host == "127.0.0.1"
    assert 4400 > crate.addresses["transport"].port >= 4300


def test_cursor(crate_cursor):
    crate_cursor.execute("SELECT 1")
    assert crate_cursor.fetchone() == [1]


def test_execute(crate_execute, crate_cursor):
    for stmt in [
        "CREATE TABLE pytest (name STRING, version INT)",
        "INSERT INTO pytest (name, version) VALUES ('test_execute', 1)",
        "REFRESH TABLE pytest",
    ]:
        crate_execute(stmt)
    crate_cursor.execute("SELECT name, version FROM pytest")
    assert crate_cursor.fetchall() == [["test_execute", 1]]
