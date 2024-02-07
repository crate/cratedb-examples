# CrateDB Examples

## About

A collection of clear and concise examples how to work with
[CrateDB](https://github.com/crate/crate). You can use them as
blueprints for your own projects.

## Layout

-   The `by-language` folder contains demo programs / technical
    investigations outlining how to get started quickly with CrateDB
    using different programming languages and frameworks.
-   The `stacks` folder contains more grown-up, complete usage scenarios
    where CrateDB is part of a larger software stack. Those resources
    may also be used within \"reference architecture\" types of
    documentation.
-   The `testing` folder contains reference implementations about how to
    use different kinds of test layers for testing your applications
    with CrateDB.

## Testing

The repository includes an universal test runner, which can be used to
invoke test suites of different languages and environments.

Before running the examples on your workstation, make sure you are using
an up-to-date version of CrateDB:

    docker pull crate/crate:nightly

Examples:

    ngr test by-language/csharp-npgsql
    ngr test by-language/csharp-npgsql --npgsql-version=6.0.9
    ngr test by-language/java-jdbc
    ngr test by-language/java-jooq
    ngr test by-language/php-amphp
    ngr test by-language/php-pdo
    ngr test by-language/python-sqlalchemy
    ngr test by-language/ruby

More examples:

    ngr test topic/machine-learning/llm-langchain
    ngr test testing/testcontainers/java

It is recommended to invoke `ngr` from within a Python virtualenv.
