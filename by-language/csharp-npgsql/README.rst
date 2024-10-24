.. highlight: console

#######################################################
Basic example for connecting to CrateDB using .NET (C#)
#######################################################


*****
About
*****

The file ``DemoProgram.cs`` is a demonstration program written in `C#`_ which
outlines typical, very basic usage scenarios with CrateDB.


Compatibility notes
===================

CrateDB versions prior to 4.2 needed a custom fork of the official Npgsql .NET
data provider for PostgreSQL, `crate-npgsql`_. CrateDB versions 4.2 and later
work with the vanilla `Npgsql - .NET Access to PostgreSQL`_ driver without the
need for a plugin.

Please note that Npgsql 5 is not supported starting with CrateDB 4.8.4, you
will need Npgsql 6 or newer.

.NET 7, 8, and 9 are supported, .NET 3.1, 4.6, 5.0, and 6.0 may still work.


*****
Usage
*****

To invoke a CrateDB instance for evaluation purposes, run::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest

Invoke example program::

    dotnet run --framework=net8.0

To connect to CrateDB Cloud, use a command like::

    dotnet run --framework=net8.0 -- \
        --host=clustername.aks1.westeurope.azure.cratedb.net --ssl-mode=Require \
        --username=foobar --password='X8F%Shn)TESTvF5ac7%eW4NM'

Explore all available connection options::

    dotnet run --framework=net8.0 -- --help


Tests
=====

For running the test scenarios wrapped into a xUnit test suite, invoke::

    dotnet test --framework=net8.0

To generate a Cobertura code coverage report, run::

    dotnet test --framework=net8.0 --collect:"XPlat Code Coverage"

For running the tests against a remote database, use, for example::

    export CRATEDB_DSN='Host=clustername.aks1.westeurope.azure.cratedb.net;Port=5432;SSL Mode=Require;Username=foobar;Password=X8F%Shn)TESTvF5ac7%eW4NM;Database=testdrive'
    dotnet test --framework=net8.0


.. _C#: https://en.wikipedia.org/wiki/C_Sharp_(programming_language)
.. _crate-npgsql: https://github.com/crate/crate-npgsql
.. _Npgsql - .NET Access to PostgreSQL: https://github.com/npgsql/npgsql
