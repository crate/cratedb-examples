import os
import time
from pathlib import Path

import pytest

from cratedb_toolkit.io.sql import DatabaseAdapter
from pueblo.testing.folder import str_list, list_notebooks, list_python_files
from pueblo.testing.snippet import pytest_module_function, pytest_notebook

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


@pytest.mark.parametrize("notebook", str_list(list_notebooks(HERE)))
def test_notebook(request, notebook: str):
    """
    From individual Jupyter Notebook file, collect cells as pytest
    test cases, and run them.

    Not using `NBRegressionFixture`, because it would manually need to be configured.
    """
    pytest_notebook(request=request, filepath=notebook)


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
