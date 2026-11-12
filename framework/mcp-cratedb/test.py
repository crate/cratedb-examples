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

    # Validate output specific to CrateDB.
    assert b"Calling tool: query_sql" in p.stdout
    assert b"cols:" in p.stdout
    assert b"rows:" in p.stdout
    assert b"Mont Blanc" in p.stdout

    assert b"Calling tool: list_schemas" in p.stdout
    assert b"- schema_name: public" in p.stdout

    assert b"Calling tool: list_tables" in p.stdout
    assert b"- name: mcp_builtin" in p.stdout

    assert b"Calling tool: describe_table" in p.stdout
    assert b'CREATE TABLE IF NOT EXISTS \\"public\\".\\"mcp_builtin\\"' in p.stdout
    assert b"primary_shards: 4" in p.stdout

    assert b"Calling tool: get_cluster_health" in p.stdout
    assert b"underreplicated_shards" in p.stdout
