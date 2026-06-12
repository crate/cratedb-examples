package cratedb

import (
	"context"
	"testing"
	"time"
)

// Advanced CrateDB types.
//
// Exercise CrateDB-specific column types over the PostgreSQL wire protocol:
// ARRAY, OBJECT(DYNAMIC), GEO_POINT and TIMESTAMP WITH TIME ZONE. Composite
// values are written with CrateDB SQL literals and read back through scalar
// CrateDB functions (array_length, object subscripts, longitude/latitude), so
// the test doesn't depend on driver-side decoding of arrays or objects.
func TestAdvancedTypes(t *testing.T) {
	ctx := context.Background()

	const ddl = `CREATE TABLE IF NOT EXISTS doc.alltypes (
		name TEXT PRIMARY KEY,
		tags ARRAY(INTEGER),
		props OBJECT(DYNAMIC) AS (kind TEXT, height INTEGER),
		location GEO_POINT,
		created_at TIMESTAMP WITH TIME ZONE
	) WITH (number_of_replicas = 0)`
	if _, err := sharedConn.Exec(ctx, ddl); err != nil {
		t.Fatalf("create table: %v", err)
	}
	t.Cleanup(func() {
		_, _ = sharedConn.Exec(ctx, "DROP TABLE IF EXISTS doc.alltypes")
	})

	const insert = `INSERT INTO doc.alltypes (name, tags, props, location, created_at) VALUES (
		'mont-blanc',
		[1, 2, 3],
		{"kind" = 'mountain', "height" = 4808},
		[6.8650, 45.8326],
		'2026-06-11T08:30:00+00:00'
	)`
	if _, err := sharedConn.Exec(ctx, insert); err != nil {
		t.Fatalf("insert: %v", err)
	}
	if _, err := sharedConn.Exec(ctx, "REFRESH TABLE doc.alltypes"); err != nil {
		t.Fatalf("refresh: %v", err)
	}

	var (
		kind     string
		height   int
		tagCount int
		lon      float64
		lat      float64
		created  time.Time
	)
	err := sharedConn.QueryRow(ctx, `SELECT
		props['kind'],
		props['height'],
		array_length(tags, 1),
		longitude(location),
		latitude(location),
		created_at
		FROM doc.alltypes WHERE name = 'mont-blanc'`).
		Scan(&kind, &height, &tagCount, &lon, &lat, &created)
	if err != nil {
		t.Fatalf("select: %v", err)
	}

	if kind != "mountain" {
		t.Errorf("props['kind'] = %q, want %q", kind, "mountain")
	}
	if height != 4808 {
		t.Errorf("props['height'] = %d, want 4808", height)
	}
	if tagCount != 3 {
		t.Errorf("array_length(tags) = %d, want 3", tagCount)
	}
	if lon < 6.86 || lon > 6.87 {
		t.Errorf("longitude = %v, want ~6.865", lon)
	}
	if lat < 45.83 || lat > 45.84 {
		t.Errorf("latitude = %v, want ~45.8326", lat)
	}
	if created.Year() != 2026 || created.Month() != time.June {
		t.Errorf("created_at = %s, want June 2026", created)
	}
}
