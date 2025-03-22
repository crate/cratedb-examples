#######################
Testcontainers for Java
#######################

*How to run integration tests of Java applications with CrateDB.*


*****
About
*****

Introduction
============

`Testcontainers for Java`_ is a Java library that supports JUnit tests,
providing lightweight, throwaway instances of common databases suitable
for integration testing scenarios.

The `Testcontainers CrateDB Module`_ will provide your application test
framework with a single-node `CrateDB`_ instance. You will be able to choose
the `CrateDB OCI image`_ variant by version, or by selecting the ``nightly``
release.

What's inside
=============

This directory includes different canonical examples how to use those
components within test harnesses of custom applications using `CrateDB`_.
Currently, all test cases are based on JUnit 4. This is an enumeration
of examples you can explore here:

- ``TestClassScope``: Class-scoped testcontainer instance with JUnit 4 @Rule/@ClassRule integration.
- ``TestFunctionScope``: Function-scoped testcontainer instance with JUnit 4 @Rule/@ClassRule integration.
- ``TestJdbcUrlScheme``: Database containers launched via Testcontainers "TC" JDBC URL scheme.
- ``TestManual``: Function-scoped testcontainer instance with manual setup/teardown.
- ``TestManualWithLegacyCrateJdbcDriver``:
  Function-scoped testcontainer instance with manual setup/teardown, using a custom
  ``CrateDBContainer``, which uses the `legacy CrateDB JDBC driver`_.
- ``TestSharedSingleton`` [1]:
  Testcontainer instance shared across multiple test classes, implemented using the Singleton pattern.
- ``TestSharedSingletonEnvironmentVersion``:
  Testcontainer instance honoring the ``CRATEDB_VERSION`` environment variable, suitable
  for running a test matrix on different versions of CrateDB, shared across multiple test
  classes.
- ``TestSqlInitialization``: Demonstrate different ways how Testcontainers can run an init script after
  the database container is started, but before your code initiates a connection to it.

[1]: Sometimes, it might be useful to define a container that is only started once for
several test classes. There is no special support for this use case provided by
the Testcontainers extension. Instead, this can be implemented using the Singleton
pattern. See also `Testcontainers » Manual container lifecycle control » Singleton
containers`_.


*****
Usage
*****

1. Make sure Java 17 is installed.
2. Invoke software tests, using `Testcontainers for Java`_. It should work out
   of the box::

    # Run all tests.
    ./gradlew test

    # Run individual tests.
    ./gradlew test --tests TestFunctionScope

    # Inspect tracebacks on failures.
    ./gradlew test --tests TestFunctionScope --info

    # Run test case showing how to select CrateDB version per environment variable.
    export CRATEDB_VERSION=5.10.3
    export CRATEDB_VERSION=nightly
    ./gradlew test --tests TestSqlInitialization

3. Invoke example application::

    # Start CrateDB.
    docker run -it --rm --publish=4200:4200 --publish=5432:5432 \
      crate:latest -Cdiscovery.type=single-node

    # Run example program, using both the CrateDB legacy
    # JDBC driver, and the vanilla PostgreSQL JDBC driver.
    ./gradlew run --args="jdbc:crate://localhost:5432/"
    ./gradlew run --args="jdbc:postgresql://localhost:5432/"


.. _CrateDB: https://github.com/crate/crate
.. _CrateDB OCI image: https://hub.docker.com/_/crate
.. _legacy CrateDB JDBC driver: https://crate.io/docs/jdbc/
.. _Testcontainers for Java: https://github.com/testcontainers/testcontainers-java
.. _Testcontainers CrateDB Module: https://www.testcontainers.org/modules/databases/cratedb/
.. _Testcontainers » Manual container lifecycle control » Singleton containers: https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers
