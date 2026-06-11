# Testcontainers for Go

*How to run integration tests of Go applications with CrateDB.*

## About

[Testcontainers for Go] provides lightweight, throwaway instances of databases
(and anything else that runs in a container) for integration testing. These
examples spin up a single-node [CrateDB] and talk to it over the PostgreSQL
wire protocol using [pgx], the canonical PostgreSQL driver for Go.

Testcontainers for Go has **no dedicated CrateDB module**, so the helper in
[`cratedb.go`](cratedb.go) drives the core `GenericContainer` with the
[CrateDB OCI image], a single-node command line, and an HTTP wait strategy on
port 4200.

## What's inside

- [`cratedb.go`](cratedb.go) — `RunCrateDB(ctx)` plus `ConnectionString` /
  `HTTPEndpoint` helpers, and `CRATEDB_VERSION`-driven image selection.
- [`shared_test.go`](shared_test.go) — **shared container**: one CrateDB started
  once per package via `TestMain` and reused by all tests.
- [`function_scope_test.go`](function_scope_test.go) — **per-test container**:
  each test gets its own throwaway CrateDB, torn down via `t.Cleanup`.
- [`types_test.go`](types_test.go) — **advanced CrateDB types**: `ARRAY`,
  `OBJECT(DYNAMIC)`, `GEO_POINT`, and `TIMESTAMP WITH TIME ZONE`.
- [`http_test.go`](http_test.go) — **HTTP endpoint**: query CrateDB's native
  `/_sql` REST interface on port 4200, complementing the pgx wire-protocol
  tests.

## Usage

1. Make sure Go (1.25+) and a Docker engine are available — Testcontainers starts
   CrateDB itself, so no CrateDB needs to be running beforehand.

2. Run the tests:

   ```shell
   # Run all tests.
   go test -v ./...

   # Run an individual test.
   go test -v -run TestAdvancedTypes ./...

   # Select the CrateDB version (image tag) to test against.
   #   (unset) / nightly -> crate/crate:nightly
   #   6.2 / latest / ... -> crate:<tag>
   export CRATEDB_VERSION=6.2
   go test -v ./...

   # Keep containers around after the run for debugging.
   export TESTCONTAINERS_RYUK_DISABLED=true
   ```

3. From the repository root, the example also runs through the shared test
   runner:

   ```shell
   ngr test testing/testcontainers/go-pgx
   ```

[CrateDB]: https://github.com/crate/crate
[CrateDB OCI image]: https://hub.docker.com/_/crate
[pgx]: https://github.com/jackc/pgx
[Testcontainers for Go]: https://golang.testcontainers.org/
