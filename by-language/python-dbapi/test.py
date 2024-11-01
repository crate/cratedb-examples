import shlex
import subprocess
import pytest


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_basic():
    cmd = "time python basic.py"
    run(cmd)


def test_vector():
    cmd = "time python vector.py"
    run(cmd)
