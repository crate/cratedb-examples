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
