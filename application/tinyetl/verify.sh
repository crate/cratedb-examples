#!/bin/sh
set -e

test $(uvx crash -c 'SELECT count(*) FROM testdrive.cities' --format=json | jq '.[0].count') -eq 3
test $(uvx crash -c 'SELECT count(*) FROM testdrive.duckdb' --format=json | jq '.[0].count') -eq 6
test $(uvx crash -c 'SELECT count(*) FROM testdrive."nab-machine-failure"' --format=json | jq '.[0].count') -eq 22695
test $(uvx crash -c 'SELECT count(*) FROM testdrive.tweets' --format=json | jq '.[0].count') -eq 142
test $(uvx crash -c 'SELECT count(*) FROM testdrive.yellowcab' --format=json | jq '.[0].count') -eq 20
