package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"

	"github.com/jackc/pgx/v5"
)

func submitDdl(ctx context.Context, conn *pgx.Conn, ddl string) error {

	sql, err := os.ReadFile("setup.sql")
	if err != nil {
		log.Fatal(err)
	}

	commandTag, err := conn.Exec(ctx, string(sql))
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(commandTag)
	return nil
}

func runBulkOperations(connStr string) {

	fmt.Println("# runBulkOperations")

	num_batches := 20
	batch_size := 500

	ctx := context.Background()
	conn, err := pgx.Connect(ctx, connStr)
	if err != nil {
		log.Fatal(err)
	}

	err = submitDdl(ctx, conn, "foo")
	if err != nil {
		log.Fatal(err)
	}

	_, err = conn.Prepare(ctx, "ps1", "INSERT INTO go_users (id, name, value) VALUES ($1, $2, $3)")
	if err != nil {
		log.Fatal(err)
	}

	for b := 0; b < num_batches; b++ {
		fmt.Println("batch " + strconv.Itoa(b))

		batch := &pgx.Batch{}
		for x := 0; x < batch_size; x++ {
			id := b*x + x
			username := "user_" + strconv.Itoa(b) + "_" + strconv.Itoa(x)
			batch.Queue("ps1", id, username, rand.Float32())
		}

		br := conn.SendBatch(ctx, batch)
		_, err := br.Exec()
		if err != nil {
			log.Fatal(err)
		}
		err = br.Close()
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println()

}
