# Meltano Examples

Concise examples about working with [CrateDB] and [Meltano], for conceiving and
running flexible ELT tasks. All the recipes are using [meltano-tap-cratedb] or
[meltano-target-cratedb] for reading and writing data from/to CrateDB.

## What's inside

- `file-to-cratedb`: Acquire data from Singer File, and load it into
  CrateDB database table.

- `cratedb-to-file`: Export data from a CrateDB database table into
  different kinds of files.

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
meltano --cwd file-to-cratedb install
meltano --cwd file-to-cratedb run tap-singer-jsonl target-cratedb
```

## Software Tests
```shell
pip install -r requirements-dev.txt
poe check
```


[CrateDB]: https://cratedb.com/product
[Meltano]: https://meltano.com/
[meltano-tap-cratedb]: https://github.com/crate/meltano-tap-cratedb
[meltano-target-cratedb]: https://github.com/crate/meltano-target-cratedb
