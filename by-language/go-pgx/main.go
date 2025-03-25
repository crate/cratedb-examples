package main

import (
	"flag"
	"fmt"
)

func main() {
	hosts := flag.String("hosts", "localhost", "CrateDB hostname")
	port := flag.Int("port", 5432, "CrateDB postgres port")
	flag.Parse()
	connStr := fmt.Sprintf("postgres://crate@%s:%d/testdrive", *hosts, *port)
	runBasicQueries(connStr)
	runBulkOperations(connStr)
}
