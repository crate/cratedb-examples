"""
Using "Testcontainers for Python" with CrateDB and unittest

Build test harnesses around CrateDB using the `CrateDBTestAdapter`
exported by `cratedb-toolkit`.

https://pypi.org/project/cratedb-toolkit/
"""
import subprocess
from pprint import pprint
from unittest import TestCase

from cratedb_toolkit.testing.testcontainers.cratedb import CrateDBTestAdapter

cratedb_layer = CrateDBTestAdapter()

SQL_STATEMENT = "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3;"


def setUpModule():
    cratedb_layer.start()


def tearDownModule():
    cratedb_layer.stop()


class CrashTest(TestCase):

    def test_crash(self):
        """
        After provisioning a test instance of CrateDB, invoke `crash`.
        """
        http_url = cratedb_layer.get_http_url()
        command = f"time crash --hosts '{http_url}' --command '{SQL_STATEMENT}'"
        subprocess.check_call(command, shell=True)

    def test_sql(self):
        """
        After provisioning a test instance of CrateDB, invoke an SQL statement.
        """
        results = cratedb_layer.database.run_sql(SQL_STATEMENT, records=True)
        pprint(results)
