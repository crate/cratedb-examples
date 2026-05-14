import os
import logging
import sqlalchemy as sa
from prefect import flow

logger = logging.getLogger(__name__)


@flow(log_prints=True)
def fetch_database():
    """Fetch data from database."""
    logger.debug("Fetching data from database")

    database_url = os.getenv("CRATEDB_SQLALCHEMY_URL")
    if database_url is None:
        raise ValueError("Database URL environment variable is not set: CRATEDB_SQLALCHEMY_URL")
    engine = sa.create_engine(database_url, echo=True)

    try:
        with engine.connect() as conn:
            result = conn.execute(sa.text("SELECT 42"))
            record = result.one()
            print(record)
            # Return the results of your task to have it stored
            # and accessible on the web UI.
            return record
        logger.info("Fetched %s database rows", len(sales))
    except Exception:
        logger.exception("Database connection error")


if __name__ == "__main__":
    # Schedule workload each five seconds.
    fetch_database.serve(name="my-first-deployment", cron="* * * * * */5")
