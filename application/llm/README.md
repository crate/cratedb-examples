# Use `llm` with CrateDB

The [llm] application is a versatile swiss-army-knife-like toolkit
for interacting with large language models (LLMs).

This folder includes a few examples of how to use it for working
with CrateDB resources.

## Install

Install packages.
```shell
uv pip install -r requirements.txt
```

Enumerate available models.
```shell
llm models list
```

## Usage

Ask questions about CrateDB from the command line.

### OpenAI

Define your API key.
```shell
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

Use OpenAI GPT, executing a single prompt.
```shell
llm prompt --model gpt-4.1 --option temperature 0.0 \
  --fragment https://cdn.crate.io/about/v1/llms-full.txt \
  --system-fragment https://cdn.crate.io/about/v1/instructions-general.md \
  "CrateDB does not seem to provide an AUTOINCREMENT feature?"
```
Use OpenAI GPT, holding an ongoing chat.
```shell
llm chat --model gpt-4.1 --option temperature 0.0 \
  --fragment https://cdn.crate.io/about/v1/llms-full.txt \
  --system-fragment https://cdn.crate.io/about/v1/instructions-general.md
```

### Anthropic

Define your API key.
```shell
export ANTHROPIC_API_KEY=<YOUR_ANTHROPIC_API_KEY>
```

Use Claude Sonnet.
```shell
llm chat --model claude-4-sonnet --option temperature 0.0 \
  --fragment https://cdn.crate.io/about/v1/llms-full.txt \
  --system-fragment https://cdn.crate.io/about/v1/instructions-general.md
```

Use Claude Opus.
```shell
llm chat --model claude-4-opus --option temperature 0.0 \
  --fragment https://cdn.crate.io/about/v1/llms-full.txt \
  --system-fragment https://cdn.crate.io/about/v1/instructions-general.md
```

## Caveat

Please note the `llms-full.txt` weighs in with a large size of approx.
180,000 input tokens. For saving tokens per request, it is advised
to use the [CrateDB MCP server], which acquires documentation resources
more selectively instead of adding the whole blob to the LLM prompt.

## Example questions

Enjoy conversations with CrateDB's documentation (talk to your knowledgebase).

- CrateDB does not seem to provide an AUTOINCREMENT feature?
- How do I use CrateDB with SQLAlchemy?

If you are running out of questions, get inspired by the standard library.
```shell
uvx 'cratedb-about>=0.0.8' list-questions
```


[CrateDB MCP server]: https://cratedb.com/docs/guide/integrate/mcp/cratedb-mcp.html
[llm]: https://pypi.org/project/llm/
