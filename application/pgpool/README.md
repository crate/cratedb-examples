# Using Pgpool-II with CrateDB

## About

[Pgpool-II] is a transparent proxy server for PostgreSQL, also
called "middleware". Its [In Memory Query Cache] is useful if you
need to serve read queries lightning fast from shared memory or
memcached, and don't want to bother your database cluster with
this database workload too much.

For example, intense dashboarding applications can profit from
query caching, in particular when system architects can't control
downstream dashboard refresh rates, or when large numbers of
clients hit the dashboard applications with redundant queries
all over again.

## What's inside

- `compose.yml`: A {Docker,Podman} Compose file that defines service
  configurations for CrateDB and Pgpool-II, and a few task definitions
  to invoke operations on the software stack:

  - `provision-functions`: Add missing function stubs to satisfy Pgpool-II.
  - `cratedb-query-data`: Submit a query to CrateDB.
  - `pgpool-query-data`: Submit a query to the Pgpool query cache.

- `test.sh`: The main test program, which starts all services, and invokes
  relevant workload tasks to provision the stack and run the experiment.
  It is also the main entrypoint for CI.

## Usage
Invoke the main entrypoint program.
```shell
sh test.sh
```
Optionally follow the log output from the services.
```shell
docker compose logs --follow
```

## Status

This experiment is just meant to run to completion and call it a day.
There are no _actual_ software tests which validate the outcome of
the last step. Corresponding test cases can be added easily at anyone's
disposal, but currently the prominent goal is just a humble exit code 0.

## Operations

To submit a query to the Pgpool query cache from your workstation,
use `localhost:5433`. From inside the container network, use `pgpool:5432`.
Example:
```shell
psql "postgresql://crate:crate@localhost:5433" <<SQL
SELECT region, mountain, height, coordinates FROM sys.summits ORDER BY height DESC LIMIT 10;
SQL
```


[In Memory Query Cache]: https://www.pgpool.net/docs/latest/en/html/runtime-in-memory-query-cache.html
[Pgpool-II]: https://pgpool.net/
