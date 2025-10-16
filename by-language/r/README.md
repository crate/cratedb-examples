# Connecting to CrateDB with R

## About

The files `basic_rpostgres.r` and `basic_rpostgresql.r` include basic
example programs that use the R packages [RPostgres] resp. [RPostgreSQL],
the canonical database interfaces and 'PostgreSQL' drivers for 'R',
to connect to CrateDB.

## Usage

Start a CrateDB instance for evaluation purposes.
```shell
docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest
```

Invoke example programs.
```shell
Rscript basic_rpostgres.r
Rscript basic_rpostgresql.r
```

Invoke software tests.
```shell
make test
```


[RPostgres]: https://cran.r-project.org/web/packages/RPostgres/
[RPostgreSQL]: https://cran.r-project.org/web/packages/RPostgreSQL/
