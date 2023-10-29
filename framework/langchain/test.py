from pathlib import Path

import pytest
from pytest_notebook.plugin import pytest_collect_file, JupyterNbTest

HERE = Path(__file__).parent


def get_all_notebooks(path: Path):
    """
    Enumerate all notebook files found in given directory.
    """
    notebooks = path.glob("**/*.ipynb")
    notebooks = [str(item.relative_to(path)) for item in notebooks]
    return notebooks


@pytest.mark.parametrize("notebook", get_all_notebooks(HERE))
def test_notebook(request, notebook: str):
    """
    From individual Jupyter Notebook file, collect cells as pytest
    test cases, and run them.

    Not using `NBRegressionFixture`, because it would manually need to be configured.
    """
    from _pytest._py.path import LocalPath
    tests = pytest_collect_file(LocalPath(notebook), request.node)
    for test in tests.collect():
        test.runtest()
