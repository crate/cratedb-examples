# Connect to CrateDB and CrateDB Cloud using ConnectorX

## About

[ConnectorX] enables you to load data from databases into Python in the
fastest and most memory efficient way.

## Usage

You can optionally accelerate the data loading using parallelism by
specifying a partition column.
```python
import connectorx as cx

cx.read_sql(
    "postgresql://username:password@server:port/database", 
    "SELECT * FROM lineitem", 
    partition_on="l_orderkey", 
    partition_num=10,
)
```
Please find more [usage examples] on the [ConnectorX documentation].

## Status

The example program `demo.py` in this folder demonstrates basic use
by reading from the built-in `sys.summits` table.

Please note many special data types have not been verified to work
with CrateDB yet, or have been identified to not work yet. We are
enumerating them within the [backlog] file.


[backlog]: ./backlog.md
[ConnectorX]: https://pypi.org/project/connectorx/
[ConnectorX documentation]: https://sfu-db.github.io/connector-x/
[usage examples]: https://sfu-db.github.io/connector-x/api.html#examples
