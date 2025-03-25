package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/jackc/pgx/v5"
)

func runBasicQueries(connStr string) {

	fmt.Println("# runBasicQueries")

	ctx := context.Background()
	conn, err := pgx.Connect(ctx, connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close(ctx)
	var name string
	err = conn.QueryRow(ctx, "select name || $1 from sys.cluster", "foo").Scan(&name)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(name)
	commandTag, err := conn.Exec(ctx, "create table if not exists t1 (x integer, ts timestamp)")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)
	ts := time.Now()
	// Convert to UTC
	loc, _ := time.LoadLocation("UTC")
	ts = ts.In(loc)
	commandTag, err = conn.Exec(ctx, "insert into t1 (x, ts) values (?, ?)", 1, ts)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)
	commandTag, err = conn.Exec(ctx, "refresh table t1")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)
	var tsRead time.Time
	err = conn.QueryRow(ctx, "select ts from t1").Scan(&tsRead)
	if err != nil {
		log.Fatal(err)
	}
	if tsRead.Sub(ts) > (1 * time.Second) {
		log.Fatal("Inserted ts doesn't match read ts: ", ts, tsRead)
	}
	commandTag, err = conn.Exec(ctx, "update t1 set x = ?", 2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)
	commandTag, err = conn.Exec(ctx, "refresh table t1")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)
	commandTag, err = conn.Exec(ctx, "delete from t1 where x = ?", 2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)

	fmt.Println()

}
