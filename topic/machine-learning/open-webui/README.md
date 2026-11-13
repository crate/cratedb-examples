# Use CrateDB with Open WebUI

## About

A complete end-to-end rig including CrateDB, the CrateDB MCP server, and Open WebUI,
including a touch of integration tests on CI/GHA.

This stack is intended solely for demonstration purposes and does **not**
implement any security hardening. Do **not** deploy it to production.

## Introduction

[Open WebUI] is an extensible, feature-rich, and user-friendly self-hosted AI
platform designed to operate entirely offline. It supports various LLM runners
like Ollama and OpenAI-compatible APIs, with built-in inference engine for RAG,
making it a powerful AI deployment solution.

The [CrateDB MCP] server gives LLM agents access to CrateDB: they can explore
schemas and tables, run read-only SQL queries, and read the CrateDB documentation.
Open WebUI connects to it over Streamable HTTP, see [Open WebUI MCP Support].
In this rig the server runs without an authentication token, so its port is not
published and only the other containers reach it.

## Usage

### Sources

It is advised to clone the Git repository and run the demo stack from there.
In this spirit, it will be easy for you to receive updates.
```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples/topic/machine-learning/open-webui
```

### Start services

Configure the API key for OpenAI within the `.env` file next to `compose.yml`
to make it persistent for unattended service operations.
```dotenv
# .env
OPENAI_API_KEY=your_openai_api_key_here
```
Or export it for a one-off run:
```shell
export OPENAI_API_KEY=your_openai_api_key_here
```

Spin up the software stack. On the first occasion, it will take a while to
download the OCI images and let Open WebUI do its thing when bootstrapping
the very first time.
```shell
docker compose up
```

### User interface

You can access the service's resources on those URLs.

- CrateDB: http://localhost:4200/
- Open WebUI: http://localhost:6200/

Explore the APIs here.

- Open WebUI: 
  - Swagger: http://localhost:6200/docs
  - OpenAPI: http://localhost:6200/openapi.json
- Jupyter:
  - http://localhost:7200/

### Configure

To make the ensemble work well, you need to configure a few bits on the Open WebUI
user interface.

- Make sure to enable the "CrateDB" tool. The toggle switch is located within the
  flyout menu on the left side of the query prompt, which can be opened using the
  `More (+)` button.

- In the "Chat Controls" flyout widget, located in the top right corner of the page,
  - make sure to enable `Function Calling: Native`, see [OPEN-WEBUI-15939],
  - and dial down to `Temperature: 0.0`.

### Example questions

Enjoy conversations with CrateDB (talk to your data) and its documentation
(talk to your knowledgebase).

- Text-to-SQL: _What is the average value for sensor 1?_
- Knowledgebase: _How do I use CrateDB with SQLAlchemy?_

### Stop services
Tear down services.
```shell
docker compose down
```
Delete all volumes.
```shell
docker compose down --volumes
```
Delete individual volumes.
```shell
docker volume rm open-webui_open-webui
```
```shell
docker volume rm open-webui_cratedb
```

### Jobs
Invoke individual jobs defined in the Compose file.
```shell
export BUILDKIT_PROGRESS=plain
docker compose run --rm setup
docker compose run --rm test
```

## What's inside

- `.env`: The dotenv file defines `OPENAI_API_KEY` for `compose.yml`.
- `compose.yml`: The service composition file defines four main services:
  CrateDB, CrateDB MCP, Open WebUI, and Jupyter. Helper jobs (setup, test, ...)
  excluded for brevity. Use it with Docker or Podman.
- `init/`: Runtime configuration snippets.


[CrateDB MCP]: https://cratedb.com/docs/guide/integrate/mcp/cratedb-mcp.html
[Open WebUI]: https://docs.openwebui.com/
[Open WebUI MCP Support]: https://docs.openwebui.com/features/extensibility/mcp/
[OPEN-WEBUI-15939]: https://github.com/open-webui/open-webui/issues/15939#issuecomment-3108279768
