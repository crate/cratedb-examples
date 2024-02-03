# Using SQL Server Integration Services with CrateDB 

## About

Microsoft [SQL Server Integration Services] (SSIS) is a component of the
Microsoft SQL Server database software that can be used to perform a broad
range of data migration tasks. [SSIS] is effectively a platform and framework
for data integration and workflow applications.

This folder includes a demo project which uses SSIS to read and write data from
[CrateDB]. The file `Package.dtsx` defines a basic [Data Flow Task] pipeline to
read data from the `"doc"."nyc_taxi"` table and write it into the
`"doc"."nyc_taxi_target"` table, in order to verify connectivity.

For connecting to CrateDB, SSIS uses the [ODBC] interface. More specifically,
because CrateDB is compatible with PostgreSQL, the [psqlODBC - PostgreSQL ODBC
driver].


[CrateDB]: https://github.com/crate/crate
[Data Flow Task]: https://learn.microsoft.com/en-us/sql/integration-services/control-flow/data-flow-task
[ODBC]: https://en.wikipedia.org/wiki/Odbc
[psqlODBC - PostgreSQL ODBC driver]: https://odbc.postgresql.org/
[SQL Server Integration Services]: https://learn.microsoft.com/en-us/sql/integration-services/sql-server-integration-services
[SSIS]: https://en.wikipedia.org/wiki/SQL_Server_Integration_Services
