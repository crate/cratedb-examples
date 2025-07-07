# Use CrateDB with ingestr

## About

[ingestr] is a command-line application that allows copying data
from any source into any destination database.

This folder includes runnable examples that use ingestr with CrateDB.
They are also used as integration tests to ensure software components
fit together well.

## Usage

To start cycling without tearing down the backend stack each time,
use the `KEEPALIVE` environment variable.
```shell
export KEEPALIVE=true
sh test.sh
```


[ingestr]: https://bruin-data.github.io/ingestr/
