# Verify Metabase with CrateDB

## About

This folder includes software integration tests for verifying
that Metabase works well together with CrateDB.
The test harness is based on Docker Compose.

## What's Inside

A basic test case that reads CrateDB's `sys.summit` table through
Metabase, after connecting CrateDB as a PostgreSQL database.

## Setup

Setup sandbox and install packages.
```bash
pip install uv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-test.txt
```

## Usage

Run integration tests.
```bash
pytest
```

Watch service logs.
```shell
docker compose logs -f
```

Note that the setup is configured to keep the containers alive after starting
them. If you want to actively recycle them, invoke `docker compose down` before
running `pytest`.
