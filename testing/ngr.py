"""
-----
About
-----

Next Generation Runner (ngr): Effortless invoke programs and test harnesses.

-------
Backlog
-------
- After a few iterations, refactor to separate package.
- Look at https://pypi.org/project/ur/
"""
import argparse
import logging
import os
import shlex
import shutil
import subprocess
import sys
import typing as t
from enum import Enum
from pathlib import Path


logger = logging.getLogger()


class ItemType(Enum):
    PYTHON = 1


class NextGenerationRunner:
    """
    Run a <thing> based on its shape.
    """

    def __init__(self, thing: t.Any, options: t.Dict) -> None:
        self.thing = thing
        self.options = options
        self.path = Path(self.thing)
        self.runner = None
        self.type: ItemType = None
        self.runners = {
            ItemType.PYTHON: PythonRunner,
        }
        self.identify()

    def identify(self) -> None:
        """
        Identify type of <thing>.
        """
        for type_, class_ in self.runners.items():
            try:
                self.runner = class_(path=self.path, options=self.options)
                self.type = self.runner.type
                break
            except:
                pass

        if self.type is None:
            raise NotImplementedError(f"Unable to identify item type. Supported types are: {list(ItemType)}")

    def run(self) -> None:
        """
        Invoke / run <thing>.
        """
        if self.path.exists():
            if self.path.is_file():
                raise NotImplementedError(f"Invoking a file is not implemented yet ;]: {self.path}")
            elif self.path.is_dir():
                logger.info(f"Invoking {self.type.name} in directory: {self.path}")
                self.runner.run()
            else:
                raise ValueError(f"Path is neither file nor directory: {self.path}")


class PythonRunner:
    """
    Basic Python runner.
    
    Currently, just knows to invoke `pytest` within a directory.
    """
    
    def __init__(self, path: Path, options: t.Dict) -> None:
        self.path = path
        self.options = options
        self.has_python_files = None
        self.has_setup_py = None
        self.has_pyproject_toml = None
        self.has_requirements_txt = None
        self.type: ItemType = None
        self.peek()

    def peek(self) -> None:
        self.has_python_files = mp(self.path, "*.py")
        self.has_setup_py = mp(self.path, "*.setup.py")
        self.has_pyproject_toml = mp(self.path, "*.pyproject.toml")
        self.has_requirements_txt = mp(self.path, "requirements*.txt")

        if self.has_python_files or self.has_setup_py or self.has_pyproject_toml or self.has_requirements_txt:
            self.type = ItemType.PYTHON

    def run(self) -> None:

        # Sanity check. When invoking a Python thing within a sandbox,
        # don't install system-wide.
        if not is_venv():
            if not self.options.get("accept_no_venv", False):
                logger.error("Unable invoke target without virtualenv. Use `--accept-no-venv` to override.")
                sys.exit(1)

        # Change working directory to designated path.
        # From there, address paths relatively.
        os.chdir(self.path)
        self.path = Path(".")

        logger.info("Installing")
        self.install()
        logger.info("Testing")
        self.test()

    def install(self) -> None:
        """
        Install dependencies of Python thing, based on its shape.
        """
        requirements_txt = list(self.path.glob("requirements*.txt"))
        if requirements_txt:
            pip_requirements_args = [f"-r {item}" for item in requirements_txt]
            pip_cmd = f"pip install {' '.join(pip_requirements_args)}"
            logger.info(f"Running pip: {pip_cmd}")
            run_command(pip_cmd)

    def test(self) -> None:
        """
        Test a Python thing, based on which test runner is installed.
        """
        has_pytest = shutil.which("pytest") is not None
        if has_pytest:
            run_command("pytest")
        else:
            raise NotImplementedError(f"No handler to invoke Python item")


def mp(path: Path, pattern: str) -> bool:
    """
    mp -- match path.

    Evaluate if path matches pattern, i.e. if the `glob` operation on a
    path yields any results.
    """
    return len(list(path.glob(pattern))) > 0


def run_command(command: str, errors="raise") -> t.Union[bool, Exception]:
    """
    A basic convenience wrapper around `subprocess.check_call`.
    """
    try:
        subprocess.check_call(shlex.split(command))
    except subprocess.CalledProcessError as ex:
        if errors == "return":
            return ex
        elif errors == "bool":
            return False
        else:
            raise
    return True


def setup_logging(level=logging.INFO, verbose: bool = False) -> None:
    """
    Set up logging subsystem.
    """
    log_format = f"%(asctime)-15s [%(name)-10s] %(levelname)-8s: %(message)s"

    if verbose:
        level = logging.DEBUG
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


def run(thing: t.Any, options: t.Dict) -> None:
    """
    Invoke the runner with a single argument, the <thing>.
    """
    ngr = NextGenerationRunner(thing=thing, options=options)
    return ngr.run()


def read_command_line_arguments():
    """
    Parse and return command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--accept-no-venv", action="store_true", help="Whether to accept not running in venv")
    return parser.parse_args()


def is_venv():
    """
    Identify whether the runner was invoked within a Python virtual environment.

    https://stackoverflow.com/a/42580137
    """
    return hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)


def main():
    """
    Main program.

    - Setup logging.
    - Read command-line parameters.
    - Run sanity checks.
    - Invoke runner.
    """
    setup_logging()
    args = read_command_line_arguments()
    if not args.target:
        logger.error("Unable to invoke target. Target not given.")
        sys.exit(1)
    run(args.target, args.__dict__)


if __name__ == "__main__":
    main()