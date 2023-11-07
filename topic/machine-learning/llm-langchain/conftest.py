# Initialize nltk upfront, so that it does not run stray output into Jupyter Notebooks.
from pueblo.testing.nlp import nltk_init

# Make `pytest.exit()` called in notebook cells gracefully skip testing the whole notebook.
from pueblo.testing.notebook import monkeypatch_pytest_notebook_treat_cell_exit_as_notebook_skip
monkeypatch_pytest_notebook_treat_cell_exit_as_notebook_skip()
