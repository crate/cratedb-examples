# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A C# demonstration project showing how to connect to [CrateDB](https://cratedb.com/) using the standard [Npgsql](https://github.com/npgsql/npgsql) .NET driver for PostgreSQL (no custom fork required for CrateDB >= 4.2). Targets the latest .NET version via `net$(NETCoreAppMaximumVersion)`.

## Commands

```bash
# Run the demo program (requires CrateDB running on localhost:5432)
dotnet run

# Connect to a remote CrateDB instance
dotnet run -- --host=clustername.aks1.westeurope.azure.cratedb.net --ssl-mode=Require \
    --username=foobar --password='password'

# Show all connection options
dotnet run -- --help

# Run all tests
dotnet test

# Run a single test by name
dotnet test --filter SystemQueryExample

# Run tests against a remote CrateDB instance
export CRATEDB_DSN='Host=host;Port=5432;SSL Mode=Require;Username=user;Password=pass;Database=testdrive'
dotnet test

# Generate Cobertura code coverage report
dotnet test --collect:"XPlat Code Coverage"
```

Start a local CrateDB instance for development:
```bash
docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest
```

## Architecture

The project is a single `.csproj` (no solution file) with source files in the root and tests in `tests/`.

**Source files:**
- `DemoProgram.cs` — Entry point (`DemoProgram.Main`) parses CLI args via `CommandLineParser`, builds an `NpgsqlDataSource` with `EnableDynamicJson()`, and runs all workload examples. Also contains `DatabaseWorkloads` with three static methods: `SystemQueryExample`, `BasicConversationExample`, `UnnestExample`.
- `DemoTypes.cs` — `DatabaseWorkloadsTypes` class demonstrating all CrateDB data types: native scalar/container/geo types, JSON via `JsonDocument`, and POCO mapping via Npgsql's dynamic JSON.
- `BasicPoco.cs` — Simple POCO used for JSON roundtrip examples.

**Tests (`tests/DemoProgramTest.cs`):**
- `DatabaseFixture` (xUnit `IClassFixture`) manages a single `NpgsqlConnection` for the test class; reads connection string from `CRATEDB_DSN` env var, falling back to `localhost`.
- Each test calls a workload method and asserts against specific expected values (e.g., `Mont Blanc - 4808` for the summits query).

## CrateDB-Specific Notes

- After `INSERT`, always issue `REFRESH TABLE <table>` before querying — CrateDB uses eventual consistency and data may not be immediately visible.
- `GEO_POINT` maps transparently to `NpgsqlPoint`.
- `GEO_SHAPE` is communicated as a JSON string over the wire. Npgsql's PostGIS plugin (`NpgsqlDbType.Geometry` / `UseGeoJson`) cannot be used because CrateDB does not expose a PostGIS `geometry` OID. Use `CrateGeoShapeExtensions` (`GeoShapeExtensions.cs`) instead:
  - **Write**: `cmd.Parameters.AddGeoShape("col", myGeoJsonNetObject)`
  - **Read**: `reader.GetGeoShape<Point>("col")`
- OBJECT/ARRAY columns are passed as `NpgsqlDbType.Json` with C# `Dictionary`, `List`, `JsonDocument`, or POCO types.
- `UNNEST(@arr1, @arr2)` is the preferred bulk-insert pattern; use `NpgsqlParameter<T[]>` for typed arrays.
- The `testdrive` schema/database is used by all examples and tests; create it in CrateDB before running if it does not exist.

## Known Limitations / TODOs

- `BIT` type handling is incomplete (commented out in `AllTypesRecord`).
- `ArrayJsonDocumentExample` is disabled — reading `character varying[]` as `List<JsonDocument>` fails.
