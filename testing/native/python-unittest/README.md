# Using "cr8" test layers with CrateDB and unittest

[cr8] provides a subsystem to invoke throwaway instances of CrateDB
for testing purposes.

This folder contains example test cases demonstrating how to use the
`create_node` utility function and the `CrateNode` class, exported
by [cr8], within your Python unittest-based test cases.

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
ngr test testing/native/python-unittest
```

Alternatively, you can change your working directory to the selected
test case folder, and run `unittest` inside there.
```shell
cd testing/native/python-unittest
python -m unittest -vvv
```


[cr8]: https://pypi.org/project/cr8/
