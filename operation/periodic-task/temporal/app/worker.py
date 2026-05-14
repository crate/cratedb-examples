# https://github.com/temporalio/documentation/tree/main/sample-apps/python/your_cron_job
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflow import CronWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="your-task-queue",
        workflows=[CronWorkflow],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

