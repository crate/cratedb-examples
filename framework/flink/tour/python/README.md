# Apache Flink and CrateDB with Python

Basic examples demonstrating how to read and write from/to
CrateDB when using Apache Flink (PyFlink).

The examples use both the [CrateDB JDBC] and the [PostgreSQL JDBC]
driver. CrateDB JDBC is needed for catalog operations, which are
required when reading from CrateDB using Flink.

```sql
uvx crash -c 'CREATE TABLE person (name STRING, age INT);'
```
Flink >= 1.19 has problems with JDBC and PyFlink,
but previous versions need a Python of the same age.
```shell
uv venv --python 3.10 --seed .venv310
uv pip install -r requirements.txt
```
```shell
python write.py
```
```shell
python ready.py
```


[CrateDB JDBC]: https://cratedb.com/docs/guide/connect/java/cratedb-jdbc.html
[PostgreSQL JDBC]: https://cratedb.com/docs/guide/connect/java/postgresql-jdbc.html
