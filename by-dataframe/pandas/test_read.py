import shlex
import subprocess

import pytest


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_read_standard():
    cmd = "time python read_pandas.py --dburi=crate://crate@localhost:4200"
    run(cmd)


@pytest.mark.skip("Needs https://github.com/crate/sqlalchemy-cratedb/pull/11")
def test_read_urllib3():
    cmd = "time python read_pandas.py --dburi=crate+urllib3://crate@localhost:4200"
    run(cmd)


@pytest.mark.skip("Needs https://github.com/crate/sqlalchemy-cratedb/pull/11")
def test_read_psycopg3():
    cmd = "time python read_pandas.py --dburi=crate+psycopg://crate@localhost:5432"
    run(cmd)
