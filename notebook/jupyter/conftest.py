import os
from pathlib import Path

import pytest
import sqlalchemy as sa
from pueblo.testing.notebook import generate_tests


def pytest_generate_tests(metafunc):
    """
    Generate pytest test case per Jupyter Notebook.
    """
    here = Path(__file__).parent
    generate_tests(metafunc, path=here)


@pytest.fixture(autouse=True)
def reset_database_tables():
    """
    Before running a test case, reset relevant tables in database.
    """

    connection_string = os.environ.get("CRATEDB_CONNECTION_STRING")

    engine = sa.create_engine(connection_string, echo=os.environ.get("DEBUG"))
    connection = engine.connect()

    reset_tables = []

    for table in reset_tables:
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {table};"))
