# Connecting to CrateDB with Go

## About

The files `test/basic_queries.go` and `test/bulk_operations.go` include
basic example programs that use the canonical PostgreSQL driver for Go,
[pgx], to connect to CrateDB.

## Usage

Start a CrateDB instance for evaluation purposes.
```shell
docker run -it --rm --publish=4200:4200 --publish=5432:5432 \
  crate:latest -Cdiscovery.type=single-node
```

Invoke example program.
```shell
go run .
```

Invoke test cases.
```shell
go test -v
```


[pgx]: https://github.com/jackc/pgx
