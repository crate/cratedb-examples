import shlex
import subprocess
import pytest


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_read_urllib3():
    cmd = "time python read_pandas.py --dburi=crate://crate@localhost:4200"
    run(cmd)


# TODO: Remove skip when psycopg dialect is released in sqlalchemy-cratedb
@pytest.mark.skip(reason="psycopg dialect not yet in released sqlalchemy-cratedb")
def test_read_psycopg3():
    cmd = "time python read_pandas.py --dburi=crate+psycopg://crate@localhost:5432"
    run(cmd)
