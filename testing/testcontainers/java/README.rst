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
framework with a single-node CrateDB instance. You will be able to choose
the `CrateDB OCI image`_ variant by version, or by selecting the ``nightly``
release.

What's inside
=============

This directory includes different canonical examples how to use those
components within test harnesses of custom applications. Currently,
all test cases are based on JUnit 4.


*****
Usage
*****

1. Make sure Java 17 is installed.
2. Run CrateDB::

       docker run -it --rm --publish=4200:4200 --publish=5432:5432 \
           crate:latest -Cdiscovery.type=single-node

3. Invoke example application::

    ./gradlew run --args="jdbc:crate://localhost:5432/"
    ./gradlew run --args="jdbc:postgresql://localhost:5432/"

4. Invoke software tests::

    # Run all tests.
    ./gradlew test

    # Run individual tests.
    ./gradlew test --tests TestFunctionScope

    # Run test case showing how to select CrateDB version per environment variable.
    export CRATEDB_VERSION=5.2.3
    export CRATEDB_VERSION=nightly
    ./gradlew test --tests TestSharedSingletonMatrix


.. _CrateDB OCI image: https://hub.docker.com/_/crate
.. _Testcontainers for Java: https://github.com/testcontainers/testcontainers-java
.. _Testcontainers CrateDB Module: https://www.testcontainers.org/modules/databases/cratedb/
