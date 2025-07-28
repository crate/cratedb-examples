import os
import time
from pathlib import Path

import pytest

from cratedb_toolkit.io.sql import DatabaseAdapter
from nbclient.exceptions import CellExecutionError
from pueblo.testing.folder import str_list, list_python_files
from pueblo.testing.notebook import generate_tests
from pueblo.testing.snippet import pytest_module_function
from testbook import testbook

HERE = Path(__file__).parent


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    return DatabaseAdapter(dburi="crate://crate@localhost:4200")


@pytest.fixture(scope="function", autouse=True)
def reset_database(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS mlb_teams_2012;")
    cratedb.run_sql("DROP TABLE IF EXISTS text_data;")
    time.sleep(0.01)


@pytest.fixture(scope="function", autouse=True)
def init_database(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql((HERE / "init.sql").read_text())


def pytest_generate_tests(metafunc):
    """
    Generate pytest test case per Jupyter Notebook.
    """
    here = Path(__file__).parent
    generate_tests(metafunc, path=here)


def test_notebook(notebook):
    """
    Execute Jupyter Notebook, one test case per .ipynb file.
    """
    # Skip Vertex AI examples, because authenticating is more complicated.
    if "vertexai" in notebook.name:
        raise pytest.skip(f"Skipping Vertex AI due to lack of authentication: {notebook.name}")

    with testbook(notebook) as tb:
        try:
            tb.execute()

        # Skip notebook if `pytest.exit()` is invoked, usually by
        # `getenvpass()`, when authentication token is not given.
        except CellExecutionError as ex:
            msg = str(ex)
            if "[skip-notebook]" in msg:
                raise pytest.skip(msg)
            raise


@pytest.mark.parametrize("pyfile", str_list(list_python_files(HERE)))
def test_file(request, cratedb, pyfile: Path):
    """
    From individual Python file, collect and wrap the `main` function into a test case.
    """

    # Skip `vector_search.py` example, when no `OPENAI_API_KEY` is supplied.
    if str(pyfile).endswith("vector_search.py"):
        if "OPENAI_API_KEY" not in os.environ:
            raise pytest.skip("OPENAI_API_KEY not given")

    pytest_module_function(request, pyfile)
