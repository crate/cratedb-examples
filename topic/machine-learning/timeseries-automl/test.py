"""
## About

Test cases for classification model examples with CrateDB, PyCaret and MLflow.


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
from pathlib import Path
import pandas as pd

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
    return DatabaseAdapter(dburi="crate://crate@localhost:4200")


@pytest.fixture(scope="function", autouse=True)
def db_reset(cratedb):
    """
    Reset database before each test case.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS sales_data_for_forecast;")


@pytest.fixture()
def forecast_dataset(cratedb):
    """
    Provide test case with a provisioned dataset.
    """
    target_data = pd.read_csv(
        "https://data.4tu.nl/file/539debdb-a325-412d-b024-593f70cba15b/a801f5d4-5dfe-412a-ace2-a64f93ad0010"
    )
    related_data = pd.read_csv(
        "https://data.4tu.nl/file/539debdb-a325-412d-b024-593f70cba15b/f2bd27bd-deeb-4933-bed7-29325ee05c2e",
        header=None,
    )
    related_data.columns = ["item", "org", "date", "unit_price"]
    data = target_data.merge(related_data, on=["item", "org", "date"])
    data["total_sales"] = data["unit_price"] * data["quantity"]
    data["date"] = pd.to_datetime(data["date"])

    # Insert the data into CrateDB
    with cratedb.engine.connect() as conn:
        data.to_sql(
            "sales_data_for_forecast",
            conn,
            index=False,
            chunksize=1000,
            if_exists="replace",
        )

    cratedb.run_sql("REFRESH TABLE sales_data_for_forecast;")


@pytest.mark.parametrize("notebook", str_list(list_notebooks(HERE)))
def test_notebook(request, notebook: str):
    """
    From individual Jupyter Notebook file, collect cells as pytest
    test cases, and run them.

    Not using `NBRegressionFixture`, because it would manually need to be configured.
    """
    pytest_notebook(request=request, filepath=notebook)


@pytest.mark.parametrize("pyfile", str_list(list_python_files(HERE)))
def test_file(request, forecast_dataset, pyfile: Path):
    """
    From individual Python file, collect and wrap the `main` function into a test case, and run it.
    """
    pytest_module_function(request, pyfile)
