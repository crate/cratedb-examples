"""
Using "Testcontainers for Python" with CrateDB and pytest

Give a test a CrateDB container of its own when it changes cluster-wide state.

A private container costs a few seconds of startup per test, so reserve it
for tests that would otherwise leave their changes behind for the others.

https://github.com/testcontainers/testcontainers-python
"""
import sqlalchemy as sa


def test_cluster_setting(private_cratedb):
    engine = sa.create_engine(private_cratedb.get_connection_url())
    with engine.connect() as connection:
        connection.execute(sa.text("SET GLOBAL TRANSIENT stats.enabled = false"))
        enabled = connection.execute(sa.text("SELECT settings['stats']['enabled'] FROM sys.cluster")).scalar()
    assert enabled is False
