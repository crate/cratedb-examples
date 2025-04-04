import shlex
import subprocess
import pytest


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_demo():
    cmd = "time python demo.py"
    run(cmd)
