# Connecting to CrateDB with R

## About

The file `basic.r` includes a basic example program that uses the R
[RPostgreSQL] package, the canonical database interface and 'PostgreSQL'
driver for 'R', to connect to CrateDB.

## Usage

Start a CrateDB instance for evaluation purposes.
```shell
docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest
```

Invoke example program.
```shell
Rscript basic.r
```

Invoke software tests.
```shell
make test
```


[RPostgreSQL]: https://cran.r-project.org/web/packages/RPostgreSQL/
