from pathlib import Path

import pytest
import sqlalchemy as sa
import sqlparse

from cratedb_toolkit.io.sql import DatabaseAdapter
from dotenv import load_dotenv

HERE = Path(__file__).parent


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    return DatabaseAdapter(dburi="crate+psycopg://crate@localhost:5432/testdrive", echo=True)


@pytest.fixture(scope="function", autouse=True)
def init_database(cratedb):
    """
    Initialize database.
    """
    # TODO: Fix `DatabaseAdapter.run_sql` to not always call `fetchall()`.
    #       psycopg3 will trip on it.
    cratedb.connection.execute(sa.text("DROP TABLE IF EXISTS time_series_data;"))
    for statement in sqlparse.split((HERE / "init.sql").read_text()):
        cratedb.connection.execute(sa.text(statement))
    cratedb.connection.commit()


def test_main(cratedb, capsys):
    """
    Execute `main.py` and verify outcome.
    """

    # Load the standalone configuration also for software testing.
    # On CI, `OPENAI_API_KEY` will need to be supplied externally.
    load_dotenv("env.standalone")

    # Invoke the workload, in-process.
    from main import main
    main()

    # Verify the outcome.
    out = capsys.readouterr().out
    assert "Answer was: The average value for sensor 1 is approximately 17.03." in out
