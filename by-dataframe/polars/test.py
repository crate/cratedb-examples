import shlex
import subprocess
import pytest
import sqlalchemy as sa


DBURI = "crate://localhost:4200"


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_read_pg():
    cmd = "time python read_pg.py"
    run(cmd)


def test_read_sqlalchemy():
    cmd = "time python read_sqlalchemy.py"
    run(cmd)


@pytest.mark.skip
def test_write_adbc(reset_table):
    cmd = "time python write_adbc.py"
    run(cmd)
    assert get_table_cardinality() == 20


def test_write_sqlalchemy(reset_table):
    cmd = "time python write_sqlalchemy.py"
    run(cmd)
    assert get_table_cardinality() == 20


@pytest.fixture
def reset_table():
    """Drop database tables used for testing."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("DROP TABLE IF EXISTS testdrive_polars;")


def get_engine():
    """Provide an SQLAlchemy `engine` instance."""
    return sa.create_engine(DBURI)


def get_table_cardinality():
    """Get number of records in table used for testing."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("REFRESH TABLE testdrive_polars;")
        result = conn.exec_driver_sql("SELECT COUNT(*) FROM testdrive_polars;")
        table_size = result.scalar_one()
        return table_size
