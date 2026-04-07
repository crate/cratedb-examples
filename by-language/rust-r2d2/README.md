# Connecting to CrateDB with Rust (r2d2)

## About

The file `src/main.rs` includes a basic example program that uses the Rust
[r2d2] and [postgres] packages, effective connecting to CrateDB by using
a client-side connection pool.

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
[r2d2]: https://crates.io/crates/r2d2
