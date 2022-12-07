.. highlight: console

#######################################################
Basic example for connecting to CrateDB using .NET (C#)
#######################################################


*****
About
*****

CrateDB versions prior to 4.2 needed a custom fork of the official Npgsql .NET
data provider for PostgreSQL, `crate-npgsql`_. CrateDB versions 4.2 and later
work with the vanilla Npgsql driver without the need for a plugin.

The file ``DemoProgram.cs`` is a demonstration program written in C# which
outlines typical, very basic usage scenarios with CrateDB.
 


*****
Usage
*****

To invoke a CrateDB instance for evaluation purposes, run::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:4.5.1

Invoke example program::

    dotnet run --framework=net5.0

To connect to CrateDB Cloud, use a command like::

    dotnet run --framework=net5.0 -- \
        --host=clustername.aks1.westeurope.azure.cratedb.net --ssl-mode=Require \
        --username=foobar --password='X8F%Shn)TESTvF5ac7%eW4NM'

Explore all available options::

    dotnet run --framework=net5.0 -- --help


Tests
=====

For running the test scenarios wrapped into a xUnit test suite, invoke::

    dotnet test --framework=net5.0

To generate a Cobertura code coverage report, run::

    dotnet test --framework=net5.0 --collect:"XPlat Code Coverage"

For running the tests against a remote database, use, for example::

    export CRATEDB_DSN='Host=clustername.aks1.westeurope.azure.cratedb.net;Port=5432;SSL Mode=Require;Username=foobar;Password=X8F%Shn)TESTvF5ac7%eW4NM;Database=testdrive'
    dotnet test --framework=net5.0


.. _crate-npgsql: https://github.com/crate/crate-npgsql
