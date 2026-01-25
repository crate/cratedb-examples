# Use Meltano to export data from CrateDB into files

## About

Export data from CrateDB into different file-based output formats, using
[meltano-tap-cratedb], [target-csv], [target-jsonl], [target-singer-jsonl],
and [target-jsonl-blob].

## Configuration

### tap-cratedb

Within the `extractors` section, at `tap-cratedb`, adjust
`config.sqlalchemy_url` to match your database connectivity settings
as pipeline source. Within the `select` section, configure which
tables you are targeting for export.

### target-{csv,jsonl}

Within the `loaders` section, at the corresponding subsections, have a look at
the relevant configuration slots `output_path_prefix`, `destination_path`,
`local.folder`, or `bucket`, to configure the filesystem destination where
export data is saved to.

## Usage

Install dependencies.
```shell
meltano install
```

Discover data schema.
```shell
meltano invoke tap-cratedb --discover > catalog.json
```

Run plugin standalone, testdrive.
```shell
meltano invoke tap-cratedb --catalog catalog.json
```

Invoke data transfer from CrateDB database to output files.
```shell
meltano run tap-cratedb target-csv
meltano run tap-cratedb target-jsonl
meltano run tap-cratedb target-singer-jsonl
```

## Screenshot

Enjoy the list of mountains.

```shell
cat output/jsonl-txt/sys-summits.jsonl | head -n 3
```

```json lines
{"classification": "I/B-07.V-B", "country": "FR/IT", "first_ascent": 1786, "height": 4808, "mountain": "Mont Blanc", "prominence": 4695, "range": "U-Savoy/Aosta", "region": "Mont Blanc massif"}
{"classification": "I/B-09.III-A", "country": "CH", "first_ascent": 1855, "height": 4634, "mountain": "Monte Rosa", "prominence": 2165, "range": "Valais", "region": "Monte Rosa Alps"}
{"classification": "I/B-09.V-A", "country": "CH", "first_ascent": 1858, "height": 4545, "mountain": "Dom", "prominence": 1046, "range": "Valais", "region": "Mischabel"}
```

## Development

In order to link the sandbox to a development installation of [meltano-tap-cratedb],
configure the `pip_url` of the component like this:

```yaml
pip_url: --editable=/path/to/sources/meltano-tap-cratedb
```


[meltano-tap-cratedb]: https://github.com/crate/meltano-tap-cratedb
[target-csv]: https://hub.meltano.com/loaders/target-csv/
[target-jsonl]: https://hub.meltano.com/loaders/target-jsonl/
[target-jsonl-blob]: https://github.com/MeltanoLabs/target-jsonl-blob
[target-singer-jsonl]: https://hub.meltano.com/loaders/target-singer-jsonl/
