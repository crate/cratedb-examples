import shlex
import subprocess
import pytest
import sqlalchemy as sa


DBURI = "crate://localhost:4200"


def run(command: str):
    subprocess.check_call(shlex.split(command))


def test_insert_dask_basic(reset_table):
    cmd = "time python insert_dask.py --mode=basic  --num-records=5000"
    run(cmd)
    assert get_table_cardinality() == 5000


def test_insert_dask_multi(reset_table):
    cmd = "time python insert_dask.py --mode=multi --num-records=5000 --bulk-size=1000"
    run(cmd)
    assert get_table_cardinality() == 5000


def test_insert_dask_bulk(reset_table):
    cmd = "time python insert_dask.py --mode=bulk --num-records=5000 --bulk-size=1000"
    run(cmd)
    assert get_table_cardinality() == 5000


def test_insert_dask_unknown(reset_table):
    cmd = "time python insert_dask.py --mode=foobar"
    with pytest.raises(subprocess.CalledProcessError) as ex:
        run(cmd)
    assert ex.match("Command.+returned non-zero exit status")


@pytest.fixture
def reset_table():
    """Drop database tables used for testing."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("DROP TABLE IF EXISTS testdrive_dask;")


def get_engine():
    """Provide an SQLAlchemy `engine` instance."""
    return sa.create_engine(DBURI)


def get_table_cardinality():
    """Get number of records in table used for testing."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("REFRESH TABLE testdrive_dask;")
        result = conn.exec_driver_sql("SELECT COUNT(*) FROM testdrive_dask;")
        table_size = result.scalar_one()
        return table_size
