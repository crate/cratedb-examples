import dataclasses
import shlex
import subprocess
import sys


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


def test_cratedb_mcp():
    """
    Validate the CrateDB MCP server works well.

    It is written in Python and uses HTTP.
    https://github.com/crate/cratedb-mcp
    """
    p = run(f"{sys.executable} example_cratedb_mcp.py")
    assert p.returncode == 0

    # Validate output specific to the MCP server.
    assert b"Processing request of type" in p.stderr
    assert b"ListPromptsRequest" in p.stderr
    assert b"ListResourcesRequest" in p.stderr
    assert b"ListToolsRequest" in p.stderr
    assert b"CallToolRequest" in p.stderr

    # Validate output specific to CrateDB.
    assert b"Calling tool: query_sql" in p.stdout
    assert b"cols:" in p.stdout
    assert b"rows:" in p.stdout
    assert b"Mont Blanc" in p.stdout

    assert b"Calling tool: get_table_metadata" in p.stdout
    assert b"- information_schema" in p.stdout
    assert b"total_missing_shards: null" in p.stdout
    assert b"table_name: table_partitions" in p.stdout

    assert b"Calling tool: get_health" in p.stdout
    assert b"underreplicated_shards" in p.stdout
