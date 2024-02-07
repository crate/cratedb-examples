# CrateDB Examples

## About

This repository contains a collection of clear and concise examples
how to work with [CrateDB](https://github.com/crate/crate). You can
use them for educational purposes, or as blueprints for your own
projects.

## Layout

-   The `by-dataframe` folder contains example code snippets how
    to work with dataframe libraries like pandas, Polars, Dask,
    Spark, and friends.

-   The `by-language` folder contains demo programs / technical
    investigations outlining how to get started quickly with CrateDB
    using different programming languages and frameworks.

-   The `framework` folder contains integration scenarios with
    full-fledged applications or software frameworks.

-   The `stacks` folder contains more grown-up, complete usage scenarios
    where CrateDB is part of a larger software stack. Those resources
    may also be used within \"reference architecture\" types of
    documentation.

-   The `testing` folder contains reference implementations about how to
    use different kinds of test layers for testing your applications
    with CrateDB.

## Testing

The repository uses an universal test runner to invoke test suites of
different languages and environments.

Before running the examples on your workstation, make sure you are using
an up-to-date version of CrateDB:

    docker pull crate/crate:nightly

### Introducing `ngr`

In order to run specific sets of test cases, you do not need to leave
the top-level directory, or run any kind of environment setup procedures.
If all goes well, just select one of the folders of interest, and invoke
`ngr test` on it, like that:

    ngr test by-language/java-jdbc
    ngr test by-language/python-sqlalchemy
    ngr test by-language/php-amphp
    ngr test by-dataframe/dask
    ngr test framework/apache-superset
    ngr test testing/testcontainers/java
    ngr test topic/machine-learning/llm-langchain

The authors recommend to invoke `ngr` from within a Python virtualenv,
in order to isolate its installation from the system Python.

### Running a Test Matrix

Some examples optionally obtain parameters on invocation time.

An example are the test cases for Npgsql, which accept the version number of
the Npgsql driver release to be obtained from the environment at runtime,
overriding any internally specified versions. Example:

    ngr test by-language/csharp-npgsql --npgsql-version=6.0.9

This feature is handy if you are running a test matrix, which is
responsible for driving the version numbers, instead of using any
versions nailed within local specification files of any sort.
