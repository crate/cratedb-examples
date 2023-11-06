from pueblo.testing.notebook import monkeypatch_pytest_notebook_treat_cell_exit_as_notebook_skip

# Make `pytest.exit()` called in notebook cells gracefully skip testing the whole notebook.
monkeypatch_pytest_notebook_treat_cell_exit_as_notebook_skip()
