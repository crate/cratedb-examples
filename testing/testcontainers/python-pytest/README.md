# Using "Testcontainers for Python" with CrateDB and pytest

*How to run integration tests of Python applications with CrateDB.*

## About

[Testcontainers for Python] provides lightweight, throwaway instances of
databases (and anything else that runs in a container) for integration
testing. Its [CrateDB module] starts a single-node [CrateDB] from the
[CrateDB OCI image], waits until its HTTP interface answers, and hands out a
connection URL for the [SQLAlchemy dialect for CrateDB].

## What's inside

- [`conftest.py`](conftest.py): the `cratedb` fixture (one container for the
  whole test session), the `private_cratedb` fixture (one container per test),
  and `cratedb_http_url`. `CRATEDB_VERSION` selects the CrateDB version.
- [`test_clients.py`](test_clients.py): the same query through three clients,
  SQLAlchemy, the [CrateDB Python driver] over HTTP, and [psycopg] over the
  PostgreSQL wire protocol.
- [`test_function_scope.py`](test_function_scope.py): a test that changes a
  cluster-wide setting, on a container of its own.
- [`test_crash.py`](test_crash.py): the [crash] command-line client against
  the shared container.

## Container scope

Starting a container takes a few seconds, so the examples show two ways to
manage CrateDB's lifecycle in a test suite:

- **Shared, session-scoped** (`cratedb`): one container is started for the
  whole test session and reused by every test that asks for it. This is the
  default, and it keeps the suite fast. Tests share state, so they must not
  depend on a clean database or leave data behind that confuses others.
- **Per-test** (`private_cratedb`): each test gets its own container, which
  is stopped when the test ends. Use it only when a test needs a pristine
  instance, for example because it changes cluster-wide settings.

## Clients

The container exposes CrateDB's HTTP interface (port 4200) and its
PostgreSQL wire protocol interface (port 5432) on random host ports.

- SQLAlchemy: `cratedb.get_connection_url()` returns a `crate://` URL.
- CrateDB Python driver: connect to `http://<host>:<port>`, using
  `cratedb.get_container_host_ip()` and `cratedb.get_exposed_port(4200)`.
- psycopg, or any other PostgreSQL client: connect to the same host and
  `cratedb.get_exposed_port(5432)`, with user `crate`.

## Usage

1. Make sure Python 3.10 or later and a Docker engine are available.
   Testcontainers starts CrateDB itself, so no CrateDB needs to be running
   beforehand.

2. Install the requirements and run the tests:

   ```shell
   git clone https://github.com/crate/cratedb-examples
   cd cratedb-examples/testing/testcontainers/python-pytest
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pytest

   # Select the CrateDB version to test against.
   #   (unset) / nightly -> crate/crate:nightly
   #   6.3 / latest / ... -> crate:<tag>
   export CRATEDB_VERSION=6.3
   pytest
   ```

3. From the repository root, the example also runs through the shared test
   runner:

   ```shell
   pip install -r requirements.txt
   ngr test testing/testcontainers/python-pytest
   ```

## cratedb-toolkit

Projects that already depend on [cratedb-toolkit] can use its
`cratedb_service` pytest fixture instead. It provides a CrateDB container
together with helpers such as `run_sql()` and `reset()`, and is installed
with `pip install 'cratedb-toolkit[testing]'`.

The [unittest example](../python-unittest) uses it. cratedb-toolkit 0.1.0
requires `testcontainers<4.15`, so it needs an environment of its own,
which is why the two examples install separately.


[crash]: https://pypi.org/project/crash/
[CrateDB]: https://github.com/crate/crate
[CrateDB module]: https://github.com/testcontainers/testcontainers-python/tree/main/src/testcontainers/community/cratedb
[CrateDB OCI image]: https://hub.docker.com/_/crate
[CrateDB Python driver]: https://pypi.org/project/crate/
[cratedb-toolkit]: https://pypi.org/project/cratedb-toolkit/
[psycopg]: https://www.psycopg.org/psycopg3/
[SQLAlchemy dialect for CrateDB]: https://pypi.org/project/sqlalchemy-cratedb/
[Testcontainers for Python]: https://testcontainers-python.readthedocs.io/
