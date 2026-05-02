# Using CrateDB with Dask Distributed

Spin up infrastructure.
```shell
export BUILDKIT_PROGRESS=plain
docker compose up --detach --wait
```

Invoke I/O payload.
```shell
docker compose run --rm export-to-deltalake
```

Verify outcome.
```shell
docker compose run --rm verify
```

Watch log files.
```shell
docker compose logs -f
```

Navigate to the Dask dashboard.
```shell
open http://localhost:8787/
```
