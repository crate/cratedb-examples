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

For building and running the demonstration program, invoke:: 

    dotnet run localhost 5432


.. _crate-npgsql: https://github.com/crate/crate-npgsql
