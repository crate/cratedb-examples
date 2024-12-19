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

The example program in this folder is validated on .NET 8 and 9,
using Npgsql 8.x and 9.x.


*****
Usage
*****

To invoke a CrateDB instance for evaluation purposes, run::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest

Invoke example program::

    dotnet run

To connect to CrateDB Cloud, use a command like::

    dotnet run -- \
        --host=clustername.aks1.westeurope.azure.cratedb.net --ssl-mode=Require \
        --username=foobar --password='X8F%Shn)TESTvF5ac7%eW4NM'

Explore all available connection options::

    dotnet run -- --help

.. note::

    Use the ``--framework=net8.0`` option to target a specific .NET framework version.

Tests
=====

For running the test scenarios wrapped into a xUnit test suite, invoke::

    dotnet test

To generate a Cobertura code coverage report, run::

    dotnet test --collect:"XPlat Code Coverage"

For running the tests against a remote database, use, for example::

    export CRATEDB_DSN='Host=clustername.aks1.westeurope.azure.cratedb.net;Port=5432;SSL Mode=Require;Username=foobar;Password=X8F%Shn)TESTvF5ac7%eW4NM;Database=testdrive'
    dotnet test

For running tests selectively, use::

    dotnet test --filter SystemQueryExample


Troubleshooting
===============

If you observe an error like this when invoking the program or test case::

    Microsoft.PackageDependencyResolution.targets(266,5): error NETSDK1005:
    Assets file '/path/to/csharp-npgsql/obj/project.assets.json' doesn't have a target for 'net9.0'.
    Ensure that restore has run and that you have included 'net9.0' in the TargetFrameworks for your project.

please adjust ``demo.csproj`` like that::

-    <TargetFramework>net$(NETCoreAppMaximumVersion)</TargetFramework>
+    <TargetFrameworks>net6.0;net8.0;net9.0</TargetFrameworks>


.. _C#: https://en.wikipedia.org/wiki/C_Sharp_(programming_language)
.. _crate-npgsql: https://github.com/crate/crate-npgsql
.. _Npgsql - .NET Access to PostgreSQL: https://github.com/npgsql/npgsql
