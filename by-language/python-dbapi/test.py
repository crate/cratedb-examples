import shlex
import subprocess
import pytest


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_select_basic():
    cmd = "time python select_basic.py"
    run(cmd)


def test_insert_basic():
    cmd = "time python insert_basic.py"
    run(cmd)
