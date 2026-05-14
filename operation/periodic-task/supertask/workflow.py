#!/usr/bin/env python3
# ruff: noqa: ERA001, T201

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "sqlalchemy-cratedb",
# ]
# ///
##
# /// task
# cron = "*/5 * * * * * *"
# [env]
# DATABASE_URL = "crate://crate:crate@cratedb:4200/"
# ///

import logging
import os
import sys
import time

import sqlalchemy as sa

logger = logging.getLogger(__name__)


class DatabaseHelloTask:
    """
    A task definition for communicating with a database.
    """

    def __init__(self, **kwargs):
        database_url = os.getenv("DATABASE_URL")
        if database_url is None:
            raise ValueError("Database URL environment variable is not set: DATABASE_URL")
        self.engine = sa.create_engine(database_url, echo=True)
        # kwargs reserved for future options

    def run(self) -> None:
        """
        Submit a dummy SQL expression to the database.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(sa.text("SELECT 42"))
                print(result.one())
        except Exception:
            logger.exception("Database connection error")
            time.sleep(1)


def run(**kwargs):
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    task = DatabaseHelloTask(**kwargs)
    task.run()


if __name__ == "__main__":
    """
    export DATABASE_URL=crate://crate@localhost:4200/
    python examples/minimal/hellodb.py
    """
    run()
