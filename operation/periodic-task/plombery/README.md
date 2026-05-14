# Periodic tasks with CrateDB and Plombery

This folder includes a collection of examples about how to schedule periodic
tasks alongside CrateDB with [Plombery].

Looks interesting as a light-weight alternative to Prefect, which
itself is a lighter-weight / more modern alternative to Airflow. 

## Launch workload

Launch scheduled workload.
```shell
docker compose up --build scheduler
```

## User interface

Navigate to http://localhost:8000/.


[Plombery]: https://lucafaggianelli.com/plombery/
