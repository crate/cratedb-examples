import os
from pathlib import Path

import pytest
from testbook import testbook


def test_notebook(notebook):
    """
    Execute Jupyter Notebook, one test case per .ipynb file.
    """
    if notebook.name == "dask-weather-data-import.ipynb":

        # Skip Kaggle tests when having no authentication information.
        kaggle_auth_exists = Path("~/.kaggle/kaggle.json").exists() or (
                "KAGGLE_USERNAME" in os.environ and "KAGGLE_KEY" in os.environ
        )
        if not kaggle_auth_exists:
            raise pytest.skip(f"Kaggle dataset can not be tested "
                              f"without authentication: {notebook.name}")

    with testbook(notebook) as tb:
        tb.execute()
