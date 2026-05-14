# https://github.com/temporalio/documentation/tree/main/sample-apps/python/your_cron_job
from temporalio import workflow


@workflow.defn
class CronWorkflow:
    @workflow.run
    async def run(self) -> None:
        print("Hello World")
