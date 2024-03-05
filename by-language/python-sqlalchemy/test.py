import shlex
import subprocess
import pytest


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_insert_efficient_multirow():
    cmd = "time python insert_efficient.py cratedb multirow"
    run(cmd)


def test_insert_efficient_batched():
    cmd = "time python insert_efficient.py cratedb batched"
    run(cmd)


def test_insert_efficient_unknown(capfd):
    cmd = "time python insert_efficient.py cratedb unknown"
    with pytest.raises(subprocess.CalledProcessError):
        run(cmd)
    out, err = capfd.readouterr()
    assert "ValueError: Unknown variant: unknown" in err


def test_sync_table():
    cmd = "time python sync_table.py urllib3 psycopg"
    run(cmd)


def test_async_table():
    cmd = "time python async_table.py psycopg asyncpg"
    run(cmd)


def test_async_streaming():
    cmd = "time python async_streaming.py psycopg asyncpg"
    run(cmd)
