package cratedb

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"net/http"
	"testing"
)

// HTTP endpoint.
//
// CrateDB's native protocol is HTTP: SQL statements are POSTed as JSON to the
// `/_sql` endpoint on port 4200.
func TestHTTPEndpoint(t *testing.T) {
	ctx := context.Background()

	endpoint, err := sharedContainer.HTTPEndpoint(ctx)
	if err != nil {
		t.Fatalf("http endpoint: %v", err)
	}

	payload, err := json.Marshal(map[string]string{
		"stmt": "SELECT mountain FROM sys.summits ORDER BY height DESC LIMIT 1",
	})
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, endpoint+"/_sql", bytes.NewReader(payload))
	if err != nil {
		t.Fatalf("build request: %v", err)
	}

	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatalf("POST /_sql: %v", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		raw, _ := io.ReadAll(resp.Body)
		t.Fatalf("status = %d, body = %s", resp.StatusCode, raw)
	}

	var result struct {
		Cols []string `json:"cols"`
		Rows [][]any  `json:"rows"`
	}
	if err = json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	if len(result.Rows) != 1 || len(result.Rows[0]) != 1 {
		t.Fatalf("unexpected result shape: cols=%v rows=%v", result.Cols, result.Rows)
	}

	if got, _ := result.Rows[0][0].(string); got != "Mont Blanc" {
		t.Errorf("highest summit = %q, want %q", got, "Mont Blanc")
	}
}
