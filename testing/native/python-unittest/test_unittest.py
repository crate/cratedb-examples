"""
Using "cr8" test layers with CrateDB and unittest

Build test harnesses around CrateDB using the `create_node`
primitive exported by `cr8`.

https://pypi.org/project/cr8/
"""
import subprocess
from unittest import TestCase

from cr8.run_crate import create_node

# Run a testing instance of CrateDB.
# TODO: How to select a nightly release?
cratedb_layer = create_node(version="latest-testing")

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
        http_url = cratedb_layer.http_url
        command = f"time crash --hosts '{http_url}' --command '{SQL_STATEMENT}'"
        subprocess.check_call(command, shell=True)
