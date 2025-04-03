#!/bin/sh
# Acquire MCP server part of `pg-mcp`.
# https://github.com/stuzero/pg-mcp
# https://github.com/crate-workbench/pg-mcp

# FIXME: Improve installation after packaging has been improved.
#        https://github.com/stuzero/pg-mcp/issues/10

rm -rf pg-mcp
git clone --depth 1 --no-checkout --filter=blob:none \
  https://github.com/crate-workbench/pg-mcp.git
cd pg-mcp
git checkout 16d7f61d5b3197777293ebae33b519f14a9d6e55 -- pyproject.toml uv.lock server test.py
uv pip install .
