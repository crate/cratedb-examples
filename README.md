<div align="center">

# CrateDB Examples

✨ _A collection of clear and concise examples how to work with [CrateDB]._ ✨

🔗 Quick links:
[Application](./application) •
[Dataframe](./by-dataframe) •
[Language](./by-language) •
[Testing](./testing) •
[Topic](./topic)

📖 More information:
[Drivers and Integrations](https://cratedb.com/docs/clients/) •
[Integration Tutorials](https://community.cratedb.com/t/overview-of-cratedb-integration-tutorials/1015) •
[Reference Documentation](https://cratedb.com/docs/crate/reference/)

</div>


## 👨‍💻 Usage

- You can explore the content by browsing folders within the repository.
  Main sections can be explored by using the quick links in the header
  area.

- If you are looking for something specific, please use GitHub search, for
  example, [searching for "jdbc"].

- You can use the code snippets for educational and knowledge base purposes,
  or as blueprints within your own projects.

- The repository is also used to support QA processes. Each example is
  designed to be invoked as an integration test case, accompanied by a
  corresponding CI validation job.


## 🧐 What's inside

This section gives you an overview about what's inside the relevant
folders.

-   **by-dataframe** contains example code snippets how
    to work with dataframe libraries like pandas, Polars, Dask,
    Spark, and friends.

-   **by-language** contains demo programs / technical
    investigations outlining how to get started quickly with CrateDB
    using different programming languages and frameworks.

-   **application** contains integration scenarios with
    full-fledged applications and software frameworks.

-   **testing** contains reference implementations about how to
    use different kinds of test layers for testing your applications
    with CrateDB.

-   **topic** mostly contains Jupyter Notebooks outlining different
    use cases around working with time-series data, and demonstrating
    machine learning technologies together with CrateDB.


## ✅ CI Status

Please visit the [Build Status] page to inspect the build status of relevant
drivers, applications, and integrations for CrateDB, on one page.


## 🏕️ Testing

In the same way as on CI, you can invoke the example programs easily on your
workstation, in order to quickly get started on behalf of working example code,
or to verify connectivity within your computing environment.

### Prerequisites

For invoking the software integration tests, you will need installations of
Docker, Python, and Git on your workstation.

Before running the tests, make sure to supply an instance of CrateDB. In order
to use and verify the most recent available code, let's select the OCI image
`crate/crate:nightly`.

```shell
docker run --rm -it --pull=always \
    --name=cratedb --publish=4200:4200 --publish=5432:5432 \
    --env=CRATE_HEAP_SIZE=4g \
    crate/crate:nightly -Cdiscovery.type=single-node
```

### Test Runner `ngr`

The repository uses a universal test runner to invoke test suites of
different languages and environments, called `ngr`.

In order to run specific sets of test cases, you do not need to leave
the top-level directory, or run any kind of environment setup procedures.
If all goes well, just select one of the folders of interest, and invoke
`ngr test` on it, like that:

    ngr test by-language/java-jdbc
    ngr test by-language/python-sqlalchemy
    ngr test by-language/php-amphp
    ngr test by-dataframe/dask
    ngr test application/apache-superset
    ngr test testing/testcontainers/java
    ngr test topic/machine-learning/llm-langchain

> [!NOTE]
> It is recommended to invoke `ngr` from within a Python virtualenv,
> in order to isolate its installation from the system Python.
> Installing `ngr` works like this:
> ```shell
> git clone https://github.com/crate/cratedb-examples
> cd cratedb-examples
> python3 -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt
> ```

### Test Matrix Support

Some examples optionally obtain parameters on invocation time.

One example is the test suite for Npgsql, which accepts the version number of
the Npgsql driver release to be obtained from the environment at runtime,
overriding any internally specified versions. Example:

    ngr test by-language/csharp-npgsql --npgsql-version=6.0.9

> [!TIP]
> This feature is handy if you are running a test matrix, which is
> responsible for driving the version numbers, instead of using the
> version numbers nailed within local specification files of any sort.


## 💁 Contributing

Interested in contributing to this project? Thanks so much for your interest! 

As an open-source project, we are always looking for improvements in form of
contributions, whether it be in the form of a new feature, improved
infrastructure, or better documentation.

Your bug reports, feature requests, and patches are greatly appreciated.


## 🌟 Contributors

[![Contributors to CrateDB Examples](https://contrib.rocks/image?repo=crate/cratedb-examples)](https://github.com/crate/cratedb-examples/graphs/contributors)


[Build Status]: https://cratedb.com/docs/crate/clients-tools/en/latest/status.html
[CrateDB]: https://github.com/crate/crate
[searching for "jdbc"]: https://github.com/search?q=repo%3Acrate%2Fcratedb-examples+jdbc
