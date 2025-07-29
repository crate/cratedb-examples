#!/usr/bin/env xonsh

# When asked about missing AUTOINCREMENT support, the
# response should include something about UUIDv7.

$XONSH_SHOW_TRACEBACK = True


# ----------
# OpenAI GPT
# ----------
response=$(
  llm prompt --model gpt-4.1 --option temperature 0.0 --no-stream \
    --fragment https://cdn.crate.io/about/v1/llms-full.txt \
    --system-fragment https://cdn.crate.io/about/v1/instructions-general.md \
    "CrateDB does not seem to provide an AUTOINCREMENT feature?"
)
print(response)
assert "UUIDv7" in response, "GPT: UUIDv7 was not in response"


# -----------------------
# Anthropic Claude Sonnet
# -----------------------
response=$(
  llm prompt --model claude-4-sonnet --option temperature 0.0 --no-stream \
    --fragment https://cdn.crate.io/about/v1/llms-full.txt \
    --system-fragment https://cdn.crate.io/about/v1/instructions-general.md \
    "CrateDB does not seem to provide an AUTOINCREMENT feature?"
)
print(response)
assert "UUIDv7" in response, "Sonnet: UUIDv7 was not in response"


# ------------
# Google Gemma
# ------------
# - Gemma3 works well for basic Text-to-SQL.
if False:
    $OLLAMA_HOST="http://100.127.86.113:11434/"
    response=$(
      llm prompt --model gemma3:1b --option temperature 0.0 --no-stream \
        --fragment sql-request.txt \
        --system "Table 'time_series_data' has columns: timestamp (TIMESTAMP), value (DOUBLE PRECISION), location (VARCHAR), sensor_id (INTEGER)" \
        "Question: What is the average value for sensor 1?"
    )
    print(response)
    assert "SQLQuery: SELECT AVG(value) FROM time_series_data WHERE sensor_id = 1" in response
