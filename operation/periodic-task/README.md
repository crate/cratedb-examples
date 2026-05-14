# Periodic tasks with CrateDB

## What's inside

This folder includes a collection of ready-to-run examples about how
to schedule periodic tasks alongside CrateDB using different periodic
task scheduler applications and frameworks.

## Usage

Most recipes provide concise `Dockerfile` blueprints, so you can easily
adapt the scheduled workloads to your needs and invoke them on the
container runtime of your choice.

If you need help to define a crontab, consider using [crontab guru]
or the [cronexpr documentation].

## Examples

```shell
export BUILDKIT_PROGRESS=plain
```

Exercise an application example using [Airflow].
```shell
docker compose --project-directory airflow up --build scheduler
```

Exercise an application example using [Plombery], based on [APScheduler].
```shell
docker compose --project-directory plombery up --build scheduler
```

Exercise an application example using [Prefect].
```shell
docker compose --project-directory prefect up --build scheduler
```

Exercise a traditional crontab-based example using [Supercronic].
```shell
docker compose --project-directory supercronic up --build scheduler
```

Exercise an application example using [Supertask], based on [APScheduler].
```shell
docker compose --project-directory supertask up --build scheduler
```

Exercise an application example using [Temporal].
```shell
docker compose --project-directory temporal up
cd temporal/app
python {cron.py,worker.py}
```


[Airflow]: https://airflow.apache.org/
[APScheduler]: https://pypi.org/project/APScheduler/
[cron]: https://en.wikipedia.org/wiki/Cron
[crontab guru]: https://crontab.guru/
[cronexpr documentation]: https://github.com/aptible/supercronic/tree/main/cronexpr
[Prefect]: https://pypi.org/project/prefect/
[Supercronic]: https://github.com/aptible/supercronic
[Supertask]: https://pypi.org/project/supertask/
[Temporal]: https://github.com/temporalio/temporal
