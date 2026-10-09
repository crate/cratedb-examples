# Using "Testcontainers for Python" with CrateDB and unittest

*How to run integration tests of Python applications with CrateDB.*

## About

[Testcontainers for Python] provides lightweight, throwaway instances of
databases (and anything else that runs in a container) for integration
testing. Its [CrateDB module] starts a single-node [CrateDB] from the
[CrateDB OCI image] and waits until its HTTP interface answers.

[`test_unittest.py`](test_unittest.py) starts one container for the test
module in `setUpModule()` and registers its stop as a module cleanup, which
runs even when a later step of the setup fails. One test
queries CrateDB through the [CrateDB Python driver], and the other through
the [crash] command-line client. `CRATEDB_VERSION` selects the CrateDB
version.

The [pytest example](../python-pytest) shows more patterns: a container per
test, other clients, and the fixture of cratedb-toolkit.

## Usage

1. Make sure Python 3.10 or later and a Docker engine are available.
   Testcontainers starts CrateDB itself, so no CrateDB needs to be running
   beforehand.

2. Install the requirements and run the tests:

   ```shell
   git clone https://github.com/crate/cratedb-examples
   cd cratedb-examples/testing/testcontainers/python-unittest
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python -m unittest -v

   # Select the CrateDB version to test against.
   #   (unset) / nightly -> crate/crate:nightly
   #   6.3 / latest / ... -> crate:<tag>
   export CRATEDB_VERSION=6.3
   python -m unittest -v
   ```

3. From the repository root, the example also runs through the shared test
   runner:

   ```shell
   pip install -r requirements.txt
   ngr test testing/testcontainers/python-unittest
   ```


[crash]: https://pypi.org/project/crash/
[CrateDB]: https://github.com/crate/crate
[CrateDB module]: https://github.com/testcontainers/testcontainers-python/tree/main/src/testcontainers/community/cratedb
[CrateDB OCI image]: https://hub.docker.com/_/crate
[CrateDB Python driver]: https://pypi.org/project/crate/
[Testcontainers for Python]: https://testcontainers-python.readthedocs.io/
