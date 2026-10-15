"""
Using "Testcontainers for Python" with CrateDB and pytest

Connect to the shared CrateDB container with three different Python clients.

- SQLAlchemy, through the `crate://` URL the container provides.
- The CrateDB Python driver, through CrateDB's HTTP interface on port 4200.
- psycopg, through the PostgreSQL wire protocol on port 5432.

https://github.com/testcontainers/testcontainers-python
"""
import psycopg
import sqlalchemy as sa
from crate import client

SQL_STATEMENT = "SELECT mountain FROM sys.summits ORDER BY height DESC LIMIT 3"
HIGHEST_SUMMITS = ["Mont Blanc", "Monte Rosa", "Dom"]


def test_sqlalchemy(cratedb):
    engine = sa.create_engine(cratedb.get_connection_url())
    with engine.connect() as connection:
        assert connection.execute(sa.text(SQL_STATEMENT)).scalars().all() == HIGHEST_SUMMITS


def test_crate_driver(cratedb_http_url):
    with client.connect(cratedb_http_url, username="crate") as connection:
        cursor = connection.cursor()
        cursor.execute(SQL_STATEMENT)
        assert [row[0] for row in cursor.fetchall()] == HIGHEST_SUMMITS


def test_psycopg(cratedb):
    host = cratedb.get_container_host_ip()
    port = cratedb.get_exposed_port(5432)
    with psycopg.connect(host=host, port=port, user="crate") as connection:
        rows = connection.execute(SQL_STATEMENT).fetchall()
        assert [row[0] for row in rows] == HIGHEST_SUMMITS
