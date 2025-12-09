# Using Readyset with CrateDB

## About

[Readyset] is a MySQL and Postgres wire-compatible caching layer that sits
in front of existing databases to speed up queries and horizontally scale
read throughput.  
It is useful if you
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
  configurations for CrateDB and Readyset, and a few task definitions
  to invoke operations on the software stack:

  - `readyset-query-data`: Submit a query to Readyset.

- `test.sh`: The main test program, which starts all services, and invokes
  relevant workload tasks to provision the stack and run the experiment.
  It is also the main entrypoint for CI.

## Status

This experiment is just meant to run to completion and call it a day.
There are no _actual_ software tests which validate the outcome of
the last step. Corresponding test cases can be added easily at anyone's
disposal, but currently the prominent goal is just a humble exit code 0.

## Operations

In order to submit a query to the Readyset query cache from your workstation,
use `localhost:5433`, while it is `readyset:5432` from inside the container
network. Example:
```shell
psql "postgresql://crate:crate@localhost:5433" <<SQL
SELECT region, mountain, height, coordinates FROM sys.summits ORDER BY height DESC LIMIT 10;
SQL
```


[Readyset]: https://github.com/readysettech/readyset
