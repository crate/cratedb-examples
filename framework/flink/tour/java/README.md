# Apache Flink and CrateDB with Java

Basic examples demonstrating how to read and write from/to
CrateDB when using Apache Flink.

The examples use both the [CrateDB JDBC] and the [PostgreSQL JDBC]
driver. CrateDB JDBC is needed for catalog operations, which are
required when reading from CrateDB using Flink.

```sql
uvx crash -c 'CREATE TABLE person (name STRING, age INT);'
```
```shell
gradle run write
```
```shell
gradle run read
```


[CrateDB JDBC]: https://cratedb.com/docs/guide/connect/java/cratedb-jdbc.html
[PostgreSQL JDBC]: https://cratedb.com/docs/guide/connect/java/postgresql-jdbc.html
