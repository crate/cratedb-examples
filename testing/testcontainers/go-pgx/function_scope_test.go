package cratedb

import (
	"context"
	"testing"

	"github.com/jackc/pgx/v5"
)

// Per-test container.
//
// Each invocation gets its own throwaway CrateDB, started inside the test and
// removed via t.Cleanup. Prefer the shared container (see TestMain) for speed;
// reach for a per-test container only when a test needs perfect isolation
// (e.g. cluster-wide settings, different CrateDB versions in one run).
func TestFunctionScope(t *testing.T) {
	ctx := context.Background()

	container, err := RunCrateDB(ctx)
	if err != nil {
		t.Fatalf("start container: %v", err)
	}

	t.Cleanup(func() {
		if err := container.Terminate(ctx); err != nil {
			t.Errorf("terminate container: %v", err)
		}
	})

	dsn, err := container.ConnectionString(ctx)
	if err != nil {
		t.Fatalf("connection string: %v", err)
	}

	conn, err := pgx.Connect(ctx, dsn)
	if err != nil {
		t.Fatalf("connect: %v", err)
	}
	defer conn.Close(ctx)

	var clusterName string
	if err := conn.QueryRow(ctx, "SELECT name FROM sys.cluster").Scan(&clusterName); err != nil {
		t.Fatalf("query sys.cluster: %v", err)
	}
	if clusterName == "" {
		t.Fatal("empty cluster name")
	}
	t.Logf("cluster name: %s", clusterName)
}
