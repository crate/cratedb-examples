# Periodic tasks with CrateDB and Temporal

This folder includes a collection of examples about how to schedule periodic
tasks alongside CrateDB with [Temporal].

## Launch system

Launch Temporal.
```shell
docker compose up
```

## User interface

To visit the user interface, navigate to http://localhost:8080/.

## Operate

To schedule a workflow, navigate to the Python application folder,
and invoke corresponding programs.
```shell
cd app
python cron.py    # To schedule a task.
python worker.py  # To process the scheduled tasks.
```

## References

- https://docs.temporal.io/cron-job
- https://docs.temporal.io/develop/python/workflows/schedules#temporal-cron-jobs


[Temporal]: https://github.com/temporalio/temporal
