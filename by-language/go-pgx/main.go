package main

import (
	"flag"
	"fmt"
)

func main() {
	hosts := flag.String("hosts", "localhost", "CrateDB hostname")
	port := flag.Int("port", 5432, "CrateDB postgres port")
	protocol_version := flag.String("protocol-version", "3.0", "PostgreSQL protocol version")
	flag.Parse()
	connStr := fmt.Sprintf(
	    "postgres://crate@%s:%d/testdrive?min_protocol_version=%s&max_protocol_version=%s",
	    *hosts, *port, *protocol_version, *protocol_version)
	runBasicQueries(connStr)
	runBulkOperations(connStr)
}
