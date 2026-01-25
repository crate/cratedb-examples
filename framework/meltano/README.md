# Meltano Examples

Concise examples about working with [CrateDB] and [Meltano], for conceiving and
running flexible ELT tasks. All the recipes are using [meltano-target-cratedb]
for reading and writing data from/to CrateDB.

## What's inside

- `singerfile-to-cratedb`: Acquire data from Singer File, and load it into
  CrateDB database table.

- `github-to-cratedb`: Acquire repository metadata from GitHub API, and load
  it separated per entity into 32 CrateDB database tables.

## Prerequisites

Before running the examples within the subdirectories, make sure to install
Meltano and its dependencies.

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Then, explore the individual Meltano projects, either invoke them from within
their directories, or by using the `--cwd` option from the root folder.

```shell
meltano --cwd github-to-cratedb install
meltano --cwd github-to-cratedb run tap-github target-cratedb
```

## Software Tests
```shell
pip install -r requirements-dev.txt
poe check
```


[CrateDB]: https://cratedb.com/product
[Meltano]: https://meltano.com/
[meltano-target-cratedb]: https://github.com/crate/meltano-target-cratedb
