// Package cratedb provides a small helper for running a single-node CrateDB
// instance with Testcontainers for Go, for use in integration tests.
//
// Testcontainers for Go has no dedicated CrateDB module, so this wraps the
// core GenericContainer with the CrateDB OCI image, a single-node command
// line, and an HTTP wait strategy.
package cratedb

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/wait"
)

const (
	// httpPort is CrateDB's HTTP endpoint (admin UI, REST/crash).
	httpPort = "4200/tcp"
	// pgPort is CrateDB's PostgreSQL wire-protocol endpoint.
	pgPort = "5432/tcp"

	defaultUser     = "crate"
	defaultDatabase = "doc"
)

// imageFromEnv returns the CrateDB OCI image to run, honoring the
// CRATEDB_VERSION environment variable so a single test suite can be run
// against a matrix of CrateDB versions.
func imageFromEnv() string {
	return imageFromLabel(os.Getenv("CRATEDB_VERSION"))
}

func imageFromLabel(label string) string {
	switch label {
	case "", "nightly":
		return "crate/crate:nightly"
	default:
		return "crate:" + label
	}
}

// CrateDBContainer is a running, single-node CrateDB testcontainer.
type CrateDBContainer struct {
	testcontainers.Container
}

// RunCrateDB starts a single-node CrateDB container and blocks until its HTTP
// endpoint (port 4200) answers with HTTP 200. Always Terminate the returned
// container when done (see TestMain and the per-test examples).
func RunCrateDB(ctx context.Context) (*CrateDBContainer, error) {
	req := testcontainers.ContainerRequest{
		Image:        imageFromEnv(),
		ExposedPorts: []string{httpPort, pgPort},
		Cmd:          []string{"-Cdiscovery.type=single-node"},
		WaitingFor: wait.ForHTTP("/").
			WithPort(httpPort).
			WithStatusCodeMatcher(func(status int) bool { return status == 200 }).
			WithStartupTimeout(180 * time.Second),
	}

	container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
		ContainerRequest: req,
		Started:          true,
	})
	if err != nil {
		return nil, fmt.Errorf("start cratedb container: %w", err)
	}

	return &CrateDBContainer{Container: container}, nil
}

// ConnectionString returns a pgx/libpq-compatible URL for CrateDB's
// PostgreSQL wire-protocol endpoint (port 5432).
func (c *CrateDBContainer) ConnectionString(ctx context.Context) (string, error) {
	host, err := c.Host(ctx)
	if err != nil {
		return "", err
	}

	port, err := c.MappedPort(ctx, pgPort)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("postgres://%s@%s:%s/%s", defaultUser, host, port.Port(), defaultDatabase), nil
}

// HTTPEndpoint returns the base URL of CrateDB's HTTP endpoint (port 4200),
// e.g. for the REST `/_sql` API or the admin UI.
func (c *CrateDBContainer) HTTPEndpoint(ctx context.Context) (string, error) {
	host, err := c.Host(ctx)
	if err != nil {
		return "", err
	}

	port, err := c.MappedPort(ctx, httpPort)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("http://%s:%s", host, port.Port()), nil
}
