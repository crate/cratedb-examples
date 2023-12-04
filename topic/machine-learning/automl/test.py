"""
## About

Test cases for classification and forecasting examples with CrateDB, PyCaret, and MLflow.


## Synopsis

Run all test cases.
```
pytest
```

Run individual test cases.
```
pytest -k file
pytest -k notebook
```
"""
import os
from pathlib import Path

import pytest
from cratedb_toolkit.util import DatabaseAdapter
from pueblo.testing.folder import str_list, list_notebooks, list_python_files
from pueblo.testing.snippet import pytest_notebook, pytest_module_function

HERE = Path(__file__).parent


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    """
    Provide test cases with a connection to CrateDB, with additional tooling.
    """
    dburi = os.environ.get("CRATEDB_CONNECTION_STRING")
    return DatabaseAdapter(dburi=f"{dburi}&schema=testdrive")


@pytest.fixture(scope="function", autouse=True)
def db_reset(cratedb):
    """
    Reset database before each test case.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS pycaret_churn;")


@pytest.fixture()
def churn_dataset(cratedb):
    """
    Provide test case with a provisioned dataset.
    """
    cratedb.import_csv_pandas(
        filepath="https://github.com/crate/cratedb-datasets/raw/main/machine-learning/automl/churn-dataset.csv",
        tablename="pycaret_churn",
    )
    cratedb.run_sql("REFRESH TABLE pycaret_churn;")


@pytest.mark.parametrize("notebook", str_list(list_notebooks(HERE)))
def test_notebook(request, notebook: str):
    """
    From individual Jupyter Notebook file, collect cells as pytest
    test cases, and run them.

    Not using `NBRegressionFixture`, because it would manually need to be configured.
    """
    pytest_notebook(request=request, filepath=notebook)


@pytest.mark.parametrize("pyfile", str_list(list_python_files(HERE)))
def test_file(request, churn_dataset, pyfile: Path):
    """
    From individual Python file, collect and wrap the `main` function into a test case, and run it.
    """
    pytest_module_function(request, pyfile)
