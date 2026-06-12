package cratedb

import (
	"context"
	"fmt"
	"os"
	"slices"
	"testing"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
)

// Shared, package-scoped container.
//
// One CrateDB container is started once for the whole package via TestMain and
// torn down after all tests have run. Starting a container is expensive, so
// tests that don't need isolation share a single instance and a single
// connection (`sharedConn`). For per-test isolation, see
// function_scope_test.go. `sharedContainer` is exposed so tests can also reach
// the HTTP endpoint (see http_test.go).
var (
	sharedContainer *CrateDBContainer
	sharedConn      *pgx.Conn
)

func TestMain(m *testing.M) {
	// os.Exit skips deferred functions, so run the real setup/teardown in a
	// helper that returns the exit code and lets its defers fire first.
	os.Exit(runWithSharedContainer(m))
}

func runWithSharedContainer(m *testing.M) int {
	ctx := context.Background()

	container, err := RunCrateDB(ctx)
	if err != nil {
		fmt.Fprintf(os.Stderr, "start CrateDB: %v\n", err)
		return 1
	}
	sharedContainer = container
	defer func() {
		if err := container.Terminate(ctx); err != nil {
			fmt.Fprintf(os.Stderr, "terminate CrateDB: %v\n", err)
		}
	}()

	dsn, err := container.ConnectionString(ctx)
	if err != nil {
		fmt.Fprintf(os.Stderr, "build connection string: %v\n", err)
		return 1
	}

	sharedConn, err = pgx.Connect(ctx, dsn)
	if err != nil {
		fmt.Fprintf(os.Stderr, "connect to CrateDB: %v\n", err)
		return 1
	}
	defer sharedConn.Close(ctx)

	return m.Run()
}

// TestSharedQuerySummits queries CrateDB's built-in `sys.summits` table through
// the shared connection. The table has 9 columns, and the three highest summits
// are Mont Blanc, Monte Rosa and Dom.
func TestSharedQuerySummits(t *testing.T) {
	ctx := context.Background()

	rows, err := sharedConn.Query(ctx,
		"SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3")
	if err != nil {
		t.Fatalf("query sys.summits: %v", err)
	}
	defer rows.Close()

	fields := rows.FieldDescriptions()
	if len(fields) != 9 {
		t.Errorf("column count = %d, want 9", len(fields))
	}
	mountainCol := slices.IndexFunc(fields, func(f pgconn.FieldDescription) bool {
		return f.Name == "mountain"
	})
	if mountainCol < 0 {
		t.Fatal("no 'mountain' column in sys.summits")
	}

	var mountains []string
	for rows.Next() {
		values, err := rows.Values()
		if err != nil {
			t.Fatalf("read row: %v", err)
		}
		name, _ := values[mountainCol].(string)
		mountains = append(mountains, name)
	}
	if err := rows.Err(); err != nil {
		t.Fatalf("iterate rows: %v", err)
	}

	want := []string{"Mont Blanc", "Monte Rosa", "Dom"}
	if !slices.Equal(mountains, want) {
		t.Errorf("top summits = %v, want %v", mountains, want)
	}
	t.Logf("top summits: %v", mountains)
}
