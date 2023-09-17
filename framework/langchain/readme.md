# LangChain and CrateDB


## About LangChain

[LangChain] is an open source framework for developing applications powered
by language models. It provides a complete set of powerful and flexible
components for building context-aware, reasoning applications.

Please refer to the [LangChain documentation] for further information.

Common end-to-end use cases are:

- Analyzing structured data
- Chatbots and friends
- Document question answering

LangChain provides standard, extendable interfaces and external integrations
for the following modules, listed from least to most complex:

- [Model I/O][Model I/O]: Interface with language models
- [Retrieval][Retrieval]: Interface with application-specific data
- [Chains][Chains]: Construct sequences of calls
- [Agents][Agents]: Let chains choose which tools to use given high-level directives
- [Memory][Memory]: Persist application state between runs of a chain
- [Callbacks][Callbacks]: Log and stream intermediate steps of any chain


## What's inside

This folder provides guidelines and runnable code to get started with [LangChain]
and [CrateDB].

- [readme.md](readme.md): The file you are currently reading contains a walkthrough
  about how to get started with the LangChain framework and CrateDB, and guides you
  to corresponding example programs how to use different subsystems.
- [requirements.txt](requirements.txt): Pulls in a patched version of LangChain,
  as well as the CrateDB client driver and the `crash` command-line interface.
- [vector_store.ipynb](vector_search.ipynb): This notebook explores CrateDB's
  [`FLOAT_VECTOR`] and [`KNN_MATCH`] functionalities for storing and retrieving
  embeddings, and for conducting similarity searches.
- [document_loader.ipynb](document_loader.ipynb): The notebook about the Document
  Loader demonstrates how to query a database table in CrateDB and use it as a
  source provider for LangChain documents.
- [conversational_memory.ipynb](conversational_memory.ipynb): LangChain also
  supports managing conversation history in SQL databases. This notebook exercises
  how that works with CrateDB.
- Accompanied to the Jupyter Notebook files, there are also basic variants of
  corresponding examples, [vector_search.py](vector_search.py),
  [document_loader.py](document_loader.py), and
  [conversational_memory.py](conversational_memory.py).


## Install

In order to properly set up a sandbox environment to explore the example notebooks
and programs, it is advised to create a Python virtualenv, and install the
dependencies into it. In this way, it is easy to wipe your virtualenv and start
from scratch anytime.

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Setup

The upcoming commands expect that you are working on a terminal with
activated virtualenv.
```shell
source .venv/bin/activate
```

### CrateDB on localhost

In order to spin up a CrateDB instance without further ado, you can use
Docker or Podman.
```shell
docker run --rm -it \
  --name=cratedb --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=4g crate -Cdiscovery.type=single-node
```

### CrateDB Cloud

Todo.


[Agents]: https://python.langchain.com/docs/modules/agents/
[Callbacks]: https://python.langchain.com/docs/modules/callbacks/
[Chains]: https://python.langchain.com/docs/modules/chains/
[CrateDB]: https://github.com/crate/crate
[`FLOAT_VECTOR`]: https://crate.io/docs/crate/reference/en/master/general/ddl/data-types.html#float-vector
[`KNN_MATCH`]: https://crate.io/docs/crate/reference/en/master/general/builtins/scalar-functions.html#scalar-knn-match
[LangChain]: https://www.langchain.com/
[LangChain documentation]: https://python.langchain.com/
[Memory]: https://python.langchain.com/docs/modules/memory/
[Model I/O]: https://python.langchain.com/docs/modules/model_io/
[Retrieval]: https://python.langchain.com/docs/modules/data_connection/
