# CrateDB with SSL

## About

A service composition file (Docker or Podman) for running CrateDB
with SSL enabled, using self-signed certificates.

Accompanied are example client programs that connect to CrateDB/SSL
using the canonical `?sslmode=require` connection option parameter,
to use SSL, but turn off certificate validation. To turn it on,
use `?sslmode=verify-ca` or `?sslmode=verify-full`.

## Caveat

Note this example is not generating fresh self-signed certificates,
but uses the ones uploaded to the repository. In this spirit, anyone
spinning an environment from this example will be using the same
encryption keys. A future iteration might improve this, possibly by
using [minica].

## Usage

```shell
docker compose up
```

## Clients

Client examples adjusted to disable certificate validation, allowing
connections to the server with self-signed certificates.

- [crash] » [client_crash.sh]
- [DB API] » [client_dbapi.py]
- [SQLAlchemy] » [client_sqlalchemy.py]

## Tests

```shell
make test
```

## Rationale

When not disabling host name verification, clients will bail out with
`SSLError`/`SSLCertVerificationError`:
```text
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed
certificate in certificate chain (_ssl.c:1010).
```

## Backlog

- Documentation is currently void of relevant ready-to-run examples
  - [Install with containers](https://cratedb.com/docs/guide/install/container/)
  - [Docker install guide](https://cratedb.com/docs/guide/install/container/docker.html)
  - [SSL Reference](https://cratedb.com/docs/crate/reference/en/latest/admin/ssl.html)
- Possibly synchronize with `crate-pdo`, where this is derived from
  <https://github.com/crate/crate-pdo/tree/2.2.2/test/provisioning>


[client_crash.sh]: ./client_crash.sh
[client_dbapi.py]: ./client_dbapi.py
[client_sqlalchemy.py]: ./client_sqlalchemy.py
[crash]: https://cratedb.com/docs/crate/crash/
[DB API]: https://cratedb.com/docs/python/
[minica]: https://github.com/jsha/minica
[SQLAlchemy]: https://cratedb.com/docs/sqlalchemy-cratedb/
