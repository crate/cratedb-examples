# Meltano Singer File -> CrateDB example

## About

Import data from a file in Singer format (JSONL) into CrateDB, using
[tap-singer-jsonl] and [meltano-target-cratedb].

## Configuration

### tap-singer-jsonl

Within the `extractors` section, have a look at `tap-singer-jsonl`'s
`config.local.paths` section, how to configure JSONL files in Singer
format as pipeline source(s).

### target-cratedb

Within the `loaders` section, at `target-cratedb`, adjust
`config.sqlalchemy_url` to match your database connectivity settings
as pipeline target.

## Usage

Install dependencies.
```shell
meltano install
```

Discover data schema.
```shell
meltano invoke tap-singer-jsonl --discover > catalog.json
```

Run plugin standalone, testdrive.
```shell
meltano invoke tap-singer-jsonl --catalog catalog.json
```

Invoke data transfer to CrateDB database.
```shell
meltano run tap-singer-jsonl target-cratedb
```

## Screenshot

Enjoy the list of countries.
```sql
crash --command 'SELECT "code", "name", "capital", "emoji", "languages[1]" FROM "melty"."countries" ORDER BY "name" LIMIT 42;'
```

![image](https://github.com/crate/meltano-target-cratedb/assets/453543/fa7076cc-267e-446c-a4f3-aa1283778ace)


## Development
In order to link the sandbox to a development installation of [meltano-target-cratedb],
configure the `pip_url` of the component like this:
```yaml
pip_url: --editable=/path/to/sources/meltano-target-cratedb
```


[meltano-target-cratedb]: https://github.com/crate/meltano-target-cratedb
[tap-singer-jsonl]: https://github.com/kgpayne/tap-singer-jsonl
