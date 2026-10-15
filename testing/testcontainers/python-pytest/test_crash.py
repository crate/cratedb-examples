"""
Using "Testcontainers for Python" with CrateDB and pytest

Invoke the `crash` command-line client against the shared CrateDB container.

https://github.com/crate/crash
"""
import subprocess


def test_crash(cratedb_http_url):
    output = subprocess.check_output(
        ["crash", "--hosts", cratedb_http_url, "--format", "csv", "--command", "SELECT 1 + 1 AS two"],
        text=True,
    )
    assert output.split() == ["two", "2"]
