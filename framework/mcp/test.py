import dataclasses
import re
import shlex
import subprocess
import sys

from cratedb_toolkit.util import DatabaseAdapter


@dataclasses.dataclass
class Process:
    """
    Manage outputs of a process.
    """
    proc: subprocess.Popen
    stdout: bytes
    stderr: bytes

    @property
    def returncode(self) -> int:
        return self.proc.returncode


def run(command: str, timeout: int = 60) -> Process:
    """
    Invoke a command in a subprocess.
    """
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=timeout)
    return Process(proc, stdout, stderr)


def test_builtin():
    """
    Validate the basic built-in MCP server for PostgreSQL works well.

    It is written in TypeScript.
    https://www.npmjs.com/package/@modelcontextprotocol/server-postgres
    """
    p = run(f"{sys.executable} example_builtin.py")
    assert p.returncode == 0

    # Validate output specific to the MCP server.
    assert b"Could not roll back transaction: error: line 1:1: mismatched input 'ROLLBACK' expecting" in p.stderr

    # Validate output specific to CrateDB.
    assert b"Calling tool: query" in p.stdout
    assert b"mountain: Mont Blanc" in p.stdout
    assert b"Reading resource: postgres://crate@localhost:5432/testdrive/schema" in p.stdout
    assert b"column_name: id" in p.stdout
    assert b"data_type: integer" in p.stdout


def test_jdbc():
    """
    Validate the Quarkus MCP server for JDBC works well.

    It is written in Java.
    https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/jdbc#readme
    """
    p = run(f"{sys.executable} example_jdbc.py")
    assert p.returncode == 0

    # Validate output specific to the MCP server.
    assert re.match(br".*\[io.quarkus\] \(main\) mcp-server-jdbc 999-SNAPSHOT on JVM.*", p.stderr, re.DOTALL)

    # Validate output specific to CrateDB.
    assert b"Calling tool: database_info" in p.stdout
    assert b"database_product_name: PostgreSQL" in p.stdout
    assert b"driver_name: PostgreSQL JDBC Driver" in p.stdout
    assert b"Calling tool: describe_table" in p.stdout
    # FIXME: Problem with `SELECT current_database()`.
    #        https://github.com/crate/crate/issues/17393
    assert b"Failed to describe table: The column name current_database was not found in this ResultSet." in p.stdout
    assert b"Calling tool: read_query" in p.stdout
    assert b'mountain: Mont Blanc' in p.stdout

    # Validate database content.
    db = DatabaseAdapter("crate://crate@localhost:4200/")
    db.refresh_table("doc.testdrive")
    records = db.run_sql("SELECT * FROM doc.testdrive", records=True)
    assert len(records) >= 1
    assert records[0] == {"id": 42, "data": "foobar"}


def test_dbhub():
    """
    Validate the DBHub MCP server works well.

    DBHub is a universal database gateway implementing the Model Context
    Protocol (MCP) server interface. This gateway allows MCP-compatible
    clients to connect to and explore different databases.

    It is written in TypeScript.
    https://github.com/bytebase/dbhub
    """
    p = run(f"{sys.executable} example_dbhub.py")
    assert p.returncode == 0

    # Validate output specific to the MCP server.
    assert b"Successfully connected to PostgreSQL database" in p.stderr
    assert b"Universal Database MCP Server" in p.stderr

    # Validate output specific to CrateDB.
    assert b"Calling tool: run_query" in p.stdout
    assert b"mountain: Mont Blanc" in p.stdout

    assert b"Calling tool: list_connectors" in p.stdout
    assert b"dsn: postgres://postgres" in p.stdout

    assert b"Reading resource: db://schemas" in p.stdout
    assert b"- doc" in p.stdout
    assert b"- sys" in p.stdout
    assert b"- testdrive" in p.stdout

    assert b"Getting prompt: explain_db" in p.stdout
    assert b"Table: dbhub in schema 'testdrive'" in p.stdout
    assert b"Structure:\\n- id (integer)\\n- data (text)" in p.stdout
