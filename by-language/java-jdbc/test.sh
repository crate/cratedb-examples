#!/usr/bin/env sh

set -e

mvn exec:java -Dexec.args="--dburl 'jdbc:postgresql://localhost:5432/testdrive?protocolVersion=${POSTGRESQL_PROTOCOL_VERSION:-3.0}'"
mvn exec:java -Dexec.args="--dburl 'jdbc:crate://localhost:5432/testdrive'"
