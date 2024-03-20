import pytest
from testbook import testbook


def test_notebook(notebook):
    """
    Execute Jupyter Notebook, one test case per .ipynb file.
    """
    if notebook.name == "dask-weather-data-import.ipynb":
        raise pytest.skip("Depends on DOWNLOAD_PATH/daily_weather.parquet")
    with testbook(notebook) as tb:
        tb.execute()
