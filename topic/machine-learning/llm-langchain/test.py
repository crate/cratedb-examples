import importlib
import io
import os
import sys
from pathlib import Path
from unittest import mock

import pytest
from _pytest.python import Function

HERE = Path(__file__).parent


def list_files(path: Path, pattern: str):
    """
    Enumerate all files in given directory.
    """
    files = path.glob(pattern)
    files = [item.relative_to(path) for item in files]
    return files


def list_notebooks(path: Path):
    """
    Enumerate all Jupyter Notebook files found in given directory.
    """
    return list_files(path, "**/*.ipynb")


def list_pyfiles(path: Path):
    """
    Enumerate all regular Python files found in given directory.
    """
    pyfiles = []
    for item in list_files(path, "**/*.py"):
        if item.suffix != ".py" or item.name in ["conftest.py"] or item.name.startswith("test"):
            continue
        pyfiles.append(item)
    return pyfiles


def str_list(things):
    """
    Converge list to list of strings.
    """
    return map(str, things)


@pytest.fixture(scope="session", autouse=True)
def nltk_init():
    """
    Initialize nltk upfront, so that it does not run stray output into Jupyter Notebooks.
    """
    download_items = ["averaged_perceptron_tagger", "punkt"]
    import nltk
    for item in download_items:
        nltk.download(item)


@pytest.fixture(scope="function", autouse=True)
def db_init():
    """
    Initialize database.
    """
    run_sql(statement="DROP TABLE IF EXISTS mlb_teams_2012;")


def db_provision_mlb_teams_2012():
    """
    Provision database.
    """
    run_sql(file="mlb_teams_2012.sql")
    run_sql(statement="REFRESH TABLE mlb_teams_2012;")


def run_sql(statement: str = None, file: str = None):
    """
    Run SQL from string or file.
    """
    import crate.crash.command
    sys.argv = ["foo", "--schema=testdrive"]
    if statement:
        sys.argv += ["--command", statement]
    if file:
        sys.stdin = io.StringIO(Path(file).read_text())
    with \
            mock.patch("crate.crash.repl.SQLCompleter._populate_keywords"), \
            mock.patch("crate.crash.command.CrateShell.close"):
        try:
            crate.crash.command.main()
        except SystemExit as ex:
            if ex.code != 0:
                raise


@pytest.mark.parametrize("notebook", str_list(list_notebooks(HERE)))
def test_notebook(request, notebook: str):
    """
    From individual Jupyter Notebook file, collect cells as pytest
    test cases, and run them.

    Not using `NBRegressionFixture`, because it would manually need to be configured.
    """
    from _pytest._py.path import LocalPath
    from pytest_notebook.plugin import pytest_collect_file
    tests = pytest_collect_file(LocalPath(notebook), request.node)
    for test in tests.collect():
        test.runtest()


@pytest.mark.parametrize("pyfile", str_list(list_pyfiles(HERE)))
def test_file(request, pyfile: Path):
    """
    From individual Python file, collect and wrap the `main` function into a test case.
    """

    # TODO: Make configurable.
    entrypoint_symbol = "main"

    # Skip `vector_search.py` example, when no `OPENAI_API_KEY` is supplied.
    if str(pyfile).endswith("vector_search.py"):
        if "OPENAI_API_KEY" not in os.environ:
            raise pytest.skip("OPENAI_API_KEY not given")

    # `document_loader.py` needs provisioning.
    if str(pyfile).endswith("document_loader.py"):
        db_provision_mlb_teams_2012()

    path = Path(pyfile)
    mod = importlib.import_module(path.stem)
    fun = getattr(mod, entrypoint_symbol)
    f = Function.from_parent(request.node, name="main", callobj=fun)
    f.runtest()
