# Using ROAPI with CrateDB

## About

The miniature stack defines {Docker,Podman} services and tasks which register
data sources with ROAPI, mount them as CrateDB tables using its built-in
PostgreSQL JDBC foreign data wrapper, then queries them.

## What's inside

- `compose.yml`: A {Docker,Podman} Compose file that defines service
  configurations for CrateDB and ROAPI, and a few task definitions
  to invoke operations on the software stack:

  - `roapi-register-data`: Use ROAPI's HTTP API to register data sources.
  - `roapi-query-data`: Use ROAPI's PostgreSQL interface to probe them.
  - `cratedb-register-data`: Mount tables into CrateDB using FDW.
  - `cratedb-query-data`: Query tables in CrateDB.

- `test.sh`: The main test program, which starts all services, and invokes
  relevant workload tasks to provision the stack and run the experiment.
  It is also the main entrypoint for CI.

## Status

This experiment is just meant to run to completion and call it a day.
There are no _actual_ software tests which validate the outcome of
the last step. Corresponding test cases can be added easily at anyone's
disposal, but currently the prominent goal is just a humble exit code 0.

## See also

- https://cratedb.com/docs/guide/feature/fdw/
- https://cratedb.com/docs/crate/reference/en/latest/admin/fdw.html
- https://cratedb.com/blog/integrate-postgresql-with-cratedb-using-foreign-data-wrappers
