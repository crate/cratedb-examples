from pathlib import Path

import pytest

from cratedb_toolkit.util.database import DatabaseAdapter
from pueblo.testing.folder import str_list, list_python_files
from pueblo.testing.notebook import generate_tests
from pueblo.testing.snippet import pytest_module_function
from testbook import testbook

HERE = Path(__file__).parent


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    return DatabaseAdapter(dburi="crate://crate@localhost:4200")


@pytest.fixture(scope="function", autouse=True)
def db_init(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS machine_data;")


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
    with testbook(notebook) as tb:
        tb.execute()


@pytest.mark.parametrize("pyfile", str_list(list_python_files(HERE)))
def test_file(request, pyfile: Path):
    """
    From individual Python file, collect and wrap the `main` function into a test case.
    """
    pytest_module_function(request, pyfile)
