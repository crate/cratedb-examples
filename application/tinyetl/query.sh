#!/bin/sh
set -e

uvx crash -c 'SELECT * FROM testdrive.cities LIMIT 5;'
uvx crash -c 'SELECT * FROM testdrive.duckdb LIMIT 5;'
uvx crash -c 'SELECT * FROM testdrive."nab-machine-failure" LIMIT 5;'
uvx crash -c 'SELECT * FROM testdrive.tweets LIMIT 5;'
uvx crash -c 'SELECT * FROM testdrive.yellowcab LIMIT 5;'
