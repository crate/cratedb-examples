# Meltano GitHub -> CrateDB example

## About

Acquire repository metadata from GitHub API, and insert into CrateDB database
tables, using [meltano-target-cratedb].

It follows the canonical example demonstrated at the [Meltano Getting Started Tutorial].

## Configuration

### tap-github

For accessing the GitHub API, you will need an authentication token. It
can be acquired at [GitHub Developer Settings » Tokens].

To configure the recipe, please store it into the `TAP_GITHUB_AUTH_TOKEN`
environment variable, either interactively, or by creating a dotenv
configuration file `.env`.

```shell
TAP_GITHUB_AUTH_TOKEN='ghp_hmQR3XTFWkfIcuyjRTBuVrRt6mnL1j2mMPT8'
```

Then, in `meltano.yml`, identify the `tap-github` section in `plugins.extractors`,
and adjust the value of `config.repositories` to correspond to the repository
you intend to scrape.

### target-cratedb

Within `loaders` section `target-cratedb`, adjust `config.sqlalchemy_url` to
match your database connectivity settings.


## Usage

Install dependencies.
```shell
meltano install
```

Invoke data transfer to JSONL files.
```shell
meltano run tap-github target-jsonl
cat github-to-cratedb/output/commits.jsonl
```

Invoke data transfer to CrateDB database.
```shell
meltano run tap-github target-cratedb
```

## Screenshot

Enjoy the release notes.
```sql
SELECT repo, tag_name, body FROM melty.releases ORDER BY tag_name DESC;
```

![image](https://github.com/crate/cratedb-toolkit/assets/453543/ac37c9cc-8e42-4c7c-84aa-64498bf48f4d)

## Troubleshooting

If you see such errors on stdout, please verify your GitHub authentication
token stored within the `TAP_GITHUB_AUTH_TOKEN` environment variable.
```python
singer_sdk.exceptions.RetriableAPIError: 401 Client Error: b'{"message":"This endpoint requires you to be authenticated.","documentation_url":"https://docs.github.com/graphql/guides/forming-calls-with-graphql#authenticating-with-graphql"}' (Reason: Unauthorized) for path: /graphql cmd_type=elb consumer=False name=tap-github producer=True stdio=stderr string_id=tap-github
```

## Development
In order to link the sandbox to a development installation of [meltano-target-cratedb],
configure the `pip_url` of the component like this:
```yaml
pip_url: --editable=/path/to/sources/meltano-target-cratedb
```


[GitHub Developer Settings » Tokens]: https://github.com/settings/tokens
[Meltano Getting Started Tutorial]: https://docs.meltano.com/getting-started/part1
[meltano-target-cratedb]: https://github.com/crate/meltano-target-cratedb
[tap-github]: https://hub.meltano.com/extractors/tap-github/
[target-jsonl]: https://hub.meltano.com/loaders/target-jsonl/
