import os
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


def test_insert_pandas():
    cmd = "time python insert_pandas.py"
    run(cmd)


def test_insert_dask():
    cmd = "time python insert_dask.py"
    run(cmd)