# Use CrateDB with Open WebUI

## About

A complete end-to-end rig including CrateDB, CrateDB MCPO, and Open WebUI. 

[Open WebUI] is an extensible, feature-rich, and user-friendly self-hosted AI
platform designed to operate entirely offline. It supports various LLM runners
like Ollama and OpenAI-compatible APIs, with built-in inference engine for RAG,
making it a powerful AI deployment solution.

CrateDB MCPO is a wrapper around CrateDB MCP, publishing the exposed tools via
OpenAPI, to connect it to Open WebUI.

## What's inside

- `.env`: The dotenv file defines `OPENAI_API_KEY` for `compose.yml` and `OPEN_WEBUI_URL` for `setup.sh`.
- `compose.yml`: The service composition file defines three services: CrateDB, CrateDB MCPO, and Open WebUI.
  Use it with `docker compose` or `podman compose`.
- `setup.Dockerfile`: Container runtime definition for `setup.sh`, including all requirements.
- `setup.sh`: Program that configures Open WebUI via HTTP API.
- `tool-servers.json`: JSON snippet for configuring the CrateDB MCPO server through `/api/v1/configs/tool_servers`.

## Operate

Configure the API key for OpenAI as environment variable, or define it within
the `.env` file.
```shell
export OPENAI_API_KEY=<your_openapi_key>
```

Spin up the software stack.
```shell
docker compose up -d
```

## Usage

You can access the services and their resources on those URLs.

- CrateDB: http://localhost:4200/
- CrateDB MCPO: http://localhost:5200/docs, http://localhost:5200/openapi.json
- Open WebUI: http://localhost:6200/, http://localhost:6200/docs

## Configure

To make the ensemble work well, you need to configure a few bits on the Open WebUI
user interface after ramping up the rig.

- Make sure to enable the "CrateDB" tool on the left side of the query prompt,
  behind the "More (`+`)" button.
- Make sure to enable "Function Calling: Native" within the flyout widget about
  "Chat Controls", to be opened in the top right corner of the screen.
- If you like, you can dial down to "Temperature: 0.5".

## Example questions

Enjoy conversations with CrateDB and its documentation.

- Text-to-SQL: What is the average value for sensor 1?
- Knowledgebase: How do I use CrateDB with SQLAlchemy?


[Open WebUI]: https://docs.openwebui.com/
