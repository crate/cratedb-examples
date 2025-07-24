# Use CrateDB with Open WebUI

## About

A complete end-to-end rig including CrateDB, CrateDB MCPO, and Open WebUI,
including a touch of integration tests on CI/GHA.

This stack is intended solely for demonstration purposes and does **not**
implement any security hardening. Do **not** deploy it to production.

## Introduction

[Open WebUI] is an extensible, feature-rich, and user-friendly self-hosted AI
platform designed to operate entirely offline. It supports various LLM runners
like Ollama and OpenAI-compatible APIs, with built-in inference engine for RAG,
making it a powerful AI deployment solution.

CrateDB MCPO is an adapter wrapper around the [CrateDB MCP] server. Because
Open WebUI uses [OpenAPI Tool Servers] to integrate external tooling and data
sources into LLM agents and workflows, standard MCP servers need to adapt to
how [Open WebUI MCP Support] works.

## Usage

### Sources

It is advised to clone the Git repository and run the demo stack from there.
In this spirit, it will be easy for you to receive updates.
```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples/application/open-webui
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

- CrateDB MCPO: 
  - Swagger: http://localhost:5200/docs
  - OpenAPI: http://localhost:5200/openapi.json
- Open WebUI: 
  - Swagger: http://localhost:6200/docs
  - OpenAPI: http://localhost:6200/openapi.json

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
- `compose.yml`: The service composition file defines three services:
  CrateDB, CrateDB MCPO, and Open WebUI. Helper jobs (setup, test, ...)
  excluded for brevity. Use it with Docker or Podman.
- `init/`: Runtime configuration snippets.


[CrateDB MCP]: https://cratedb.com/docs/guide/integrate/mcp/cratedb-mcp.html
[OpenAPI Tool Servers]: https://docs.openwebui.com/openapi-servers/
[Open WebUI]: https://docs.openwebui.com/
[Open WebUI MCP Support]: https://docs.openwebui.com/openapi-servers/mcp/
[OPEN-WEBUI-15939]: https://github.com/open-webui/open-webui/issues/15939#issuecomment-3108279768
