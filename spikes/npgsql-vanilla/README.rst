#################################################################
Basic demonstration program for using CrateDB with vanilla Npgsql
#################################################################


************
Introduction
************

CrateDB versions prior to 4.2 needed a custom fork of the official Npgsql .NET
data provider for PostgreSQL, `crate-npgsql`_. CrateDB versions 4.2 and later
work with the vanilla Npgsql driver without the need for a plugin.

The file ``DemoProgram.cs`` is a demonstration program written in C# which
outlines typical, very basic usage scenarios with CrateDB.
 

*****
Usage
*****

In order to invoke a CrateDB instance for evaluation purposes, run::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:4.5.1

For building and running the demonstration program and connect to
``localhost:5432``, invoke::

    dotnet run 

In order to connect to CrateDB Cloud, use::

    dotnet run -- --host=clustername.aks1.westeurope.azure.cratedb.net --ssl-mode=Require --username=foobar --password='X8F%Shn)TESTvF5ac7%eW4NM'

For exploring all available options, run:: 

    dotnet run -- --help


.. _crate-npgsql: https://github.com/crate/crate-npgsql
