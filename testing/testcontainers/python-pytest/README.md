# Using "Testcontainers for Python" with CrateDB and pytest

[Testcontainers] is an open source framework for providing throwaway,
lightweight instances of databases, message brokers, web browsers, or
just about anything that can run in a Docker container.

This folder contains example test cases demonstrating how to use the
`cratedb_service` pytest fixture exported by [cratedb-toolkit].

> [!TIP]
> Please also refer to the header sections of each of the provided
> example programs, to learn more about what's exactly inside.


## Run Tests

Acquire the `cratedb-examples` repository, and install sandbox and
prerequisites.
```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, invoke the integration test cases.
```shell
export TC_KEEPALIVE=true
ngr test testing/testcontainers/python-pytest
```

Alternatively, you can change your working directory to the selected
test case folder, and run `pytest` inside there.
```shell
cd testing/testcontainers/python-pytest
pytest
```


[cratedb-toolkit]: https://pypi.org/project/cratedb-toolkit/
[Testcontainers]: https://testcontainers.org/
