# Connecting to CrateDB with Rust

## About

The file `src/main.rs` includes a basic example program that uses the Rust
[postgres] package, a native, synchronous PostgreSQL client, to connect to
CrateDB.

## Usage

Start a CrateDB instance for evaluation purposes.
```shell
docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest
```

Invoke example program.
```shell
cargo run
```

Invoke software tests.
```shell
cargo test
```


[postgres]: https://crates.io/crates/postgres
