import os
import sqlalchemy as sa
from apscheduler.triggers.interval import IntervalTrigger
from plombery import task, get_logger, Trigger, register_pipeline


@task
async def fetch_database():
    """Fetch data from database."""
    # using Plombery logger your logs will be stored
    # and accessible on the web UI
    logger = get_logger()
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


register_pipeline(
    id="database_pipeline",
    description="Fetch data from database",
    tasks=[fetch_database],
    triggers=[
        Trigger(
            id="random-id",
            name="Hotzenplotz",
            description="Run the pipeline every five seconds",
            schedule=IntervalTrigger(seconds=5),
        ),
    ],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("plombery:get_app", host="0.0.0.0", reload=True, factory=True)
