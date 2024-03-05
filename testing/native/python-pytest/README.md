# Using "pytest-crate" with CrateDB and pytest

[pytest-crate] wraps the CrateDB test layer from [cr8], and provides
a few pytest fixtures to conveniently make it accessible for test
cases based on pytest.

This folder contains example test cases demonstrating how to use the
`crate`, `crate_cursor`, and `crate_cursor` pytest fixtures exported
by [pytest-crate].

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
ngr test testing/native/python-pytest
```

Alternatively, you can change your working directory to the selected
test case folder, and run `pytest` inside there.
```shell
cd testing/native/python-pytest
pytest
```


[cr8]: https://pypi.org/project/cr8/
[pytest-crate]: https://pypi.org/project/pytest-crate/
