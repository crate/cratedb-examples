from pathlib import Path

import pytest

from cratedb_toolkit.io.sql import DatabaseAdapter
from dotenv import load_dotenv

HERE = Path(__file__).parent


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    return DatabaseAdapter(dburi="crate://crate@localhost:4200")


@pytest.fixture(scope="function", autouse=True)
def init_database(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS time_series_data;")
    cratedb.run_sql((HERE / "init.sql").read_text())


def test_nlsql(cratedb, capsys):
    """
    Execute `demo_nlsql.py` and verify outcome.
    """

    # Load the standalone configuration also for software testing.
    # On CI, `OPENAI_API_KEY` will need to be supplied externally.
    load_dotenv("env.standalone")

    # Invoke the workload, in-process.
    from demo_nlsql import main
    main()

    # Verify the outcome.
    out = capsys.readouterr().out
    assert "Answer was: The average value for sensor 1 is approximately 17.03." in out
