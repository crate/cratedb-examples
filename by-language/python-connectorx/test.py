import shlex
import subprocess


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_demo():
    cmd = "time python3 demo.py"
    run(cmd)
