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
from abc import abstractmethod
from enum import Enum
from pathlib import Path


logger = logging.getLogger()


class ItemType(Enum):
    DOTNET = "dotnet"
    JAVA = "java"
    PHP = "php"
    PYTHON = "python"
    RUBY = "ruby"


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
            ItemType.DOTNET: DotNetRunner,
            ItemType.JAVA: JavaRunner,
            ItemType.PHP: PhpRunner,
            ItemType.PYTHON: PythonRunner,
            ItemType.RUBY: RubyRunner,
        }
        self.identify()

    @property
    def runner_names(self):
        names = []
        for runner in self.runners.keys():
            names.append(runner.name)
        return names

    def identify(self) -> None:
        """
        Identify type of <thing>.
        """
        for type_, class_ in self.runners.items():
            logger.info(f"Probing: type={type_}, class={class_}")
            try:
                self.runner = class_(path=self.path, options=self.options)
                self.type = self.runner.type
            except:
                pass
            if self.type is not None:
                break

        if self.type is None:
            raise NotImplementedError(f"Unable to identify invocation target. Supported types are: {self.runner_names}")

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


class RunnerBase:

    def __init__(self, path: Path, options: t.Dict) -> None:
        self.path = path
        self.options = options
        self.type: ItemType = None
        if hasattr(self, "__post_init__"):
            self.__post_init__()
        self.has_makefile = mp(self.path, "Makefile")
        self.peek()

    def run(self) -> None:
        # Change working directory to designated path.
        # From there, address paths relatively.
        os.chdir(self.path)
        self.path = Path(".")

        logger.info("Environment Information")
        self.info()
        logger.info("Installing")
        self.install()
        logger.info("Testing")
        self.test()

    @abstractmethod
    def peek(self) -> None:
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def info(self) -> None:
        pass

    @abstractmethod
    def install(self) -> None:
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def test(self) -> None:
        raise NotImplementedError("Method must be implemented")


class DotNetRunner(RunnerBase):
    """
    .NET test suite runner.

    - Knows how to invoke `dotnet {restore,list,test}` appropriately.
    - Optionally accepts the `--npgsql-version=` command-line option, to specify the Npgsql version.
    """

    def __post_init__(self) -> None:
        self.has_csproj = None
        self.framework = None

    def peek(self) -> None:
        self.has_csproj = mp(self.path, "*.csproj")

        dotnet_version_full = subprocess.check_output(shlex.split("dotnet --version")).decode().strip()
        dotnet_version_major = dotnet_version_full[0]
        self.framework = f"net{dotnet_version_major}.0"

        if self.has_csproj:
            self.type = ItemType.DOTNET

    def info(self) -> None:
        """
        Display environment information.
        """
        run_command("dotnet --version")
        run_command("dotnet --info")

    def install(self) -> None:
        """
        Install dependencies from `.csproj` file.
        """
        self.adjust_npgql_version()
        run_command("dotnet restore")
        run_command("dotnet list . package")

    def adjust_npgql_version(self):
        if "npgsql_version" not in self.options:
            logger.info("[MATRIX] Not modifying Npgsql version")
            return
        npgsql_version = self.options.get("npgsql_version")
        logger.info(f"[MATRIX] Modifying Npgsql version: {npgsql_version}")
        cmd = f"""
            sed -E 's!<PackageReference Include="Npgsql" Version=".+?" />!<PackageReference Include="Npgsql" Version="{npgsql_version}" />!' \
            -i demo.csproj
        """
        run_command(cmd)

    def test(self) -> None:
        """
        Invoke `dotnet test`, with code coverage tracking.
        """
        run_command(f'dotnet test --framework={self.framework} --collect:"XPlat Code Coverage"')


class JavaRunner(RunnerBase):
    """
    Java test suite runner.

    - Knows how to invoke either Gradle or Maven.
    """

    def __post_init__(self) -> None:
        self.has_pom_xml = None
        self.has_gradle_files = None

    def peek(self) -> None:
        self.has_pom_xml = mp(self.path, "pom.xml")
        self.has_gradle_files = mp(self.path, "*.gradle")

        if self.has_pom_xml or self.has_gradle_files:
            self.type = ItemType.JAVA

    def info(self) -> None:
        """
        Display environment information.
        """
        run_command("java -version")

    def install(self) -> None:
        """
        Install dependencies.
        """
        if self.has_pom_xml:
            run_command("mvn install")
        elif self.has_gradle_files:
            run_command("./gradlew install")
        else:
            raise NotImplementedError("Unable to invoke target: install")

    def test(self) -> None:
        """
        Invoke software tests.
        """
        if self.has_makefile:
            run_command("make test")
        elif self.has_pom_xml:
            run_command(f'mvn test')
        elif self.has_gradle_files:
            run_command("./gradlew check")
        else:
            raise NotImplementedError("Unable to invoke target: test")


class PhpRunner(RunnerBase):
    """
    Basic PHP runner.

    Currently, just knows to invoke `composer` within a directory.
    """

    def __post_init__(self) -> None:
        self.has_composer_json = None

    def peek(self) -> None:
        self.has_composer_json = mp(self.path, "composer.json")

        if self.has_composer_json:
            self.type = ItemType.PHP

    def install(self) -> None:
        """
        Install dependencies of PHP Composer package.
        """
        run_command("composer install")

    def test(self) -> None:
        """
        Invoke a script called `test`, defined in `composer.json`.
        """
        run_command("composer run test")


class PythonRunner(RunnerBase):
    """
    Basic Python runner.

    Currently, just knows to invoke `pytest` within a directory.
    """

    def __post_init__(self) -> None:
        self.has_python_files = None
        self.has_setup_py = None
        self.has_pyproject_toml = None
        self.has_requirements_txt = None

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

        return super().run()

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


class RubyRunner(RunnerBase):
    """
    Basic Ruby runner.

    Currently, just knows to invoke Bundler and Rake within a directory.

    - https://bundler.io/
    - https://en.wikipedia.org/wiki/Rake_(software)
    """

    def __post_init__(self) -> None:
        self.has_gemfile = None
        self.has_rakefile = None

    def peek(self) -> None:
        self.has_gemfile = mp(self.path, "Gemfile")
        self.has_rakefile = mp(self.path, "Rakefile")

        if self.has_gemfile or self.has_rakefile:
            self.type = ItemType.RUBY

    def install(self) -> None:
        """
        Install dependencies using Ruby's Bundler, defined in `Gemfile`.
        """
        run_command("bundle install")

    def test(self) -> None:
        """
        Invoke a rake target called `test`, defined in `Rakefile`.
        """
        run_command("bundle exec rake test")


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
    logger.info(f"Running command: {command}")
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
    parser.add_argument("--npgsql-version", type=str, help="Version of Npgsql")
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

    try:
        run(args.target, args.__dict__)
    except NotImplementedError as ex:
        logger.critical(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
