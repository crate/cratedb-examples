from testbook import testbook


def test_notebook(notebook):
    """
    Execute Jupyter Notebook, one test case per .ipynb file.
    """
    with testbook(notebook) as tb:
        tb.execute()
