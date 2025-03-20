# Npgsql Entity Framework Core provider for PostgreSQL with CrateDB

## About

The file `BlogDemo.cs` includes a demonstration program written in [C#] which
demonstrates the [Entity Framework Core] README code snippet of [efcore.pg],
effectively a very basic usage scenario, with CrateDB.

`efcore.pg` is built on top of [Npgsql - .NET Access to PostgreSQL].

## Usage

Start a CrateDB instance for evaluation purposes.
```shell
docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest
```

Invoke example program.
```shell
dotnet run
```

## Tests

Invoke software tests.
```shell
dotnet test
```

Generate a Cobertura code coverage report.
```shell
dotnet test --collect:"XPlat Code Coverage"
```

Invoke test cases selectively.
```shell
dotnet test --filter BlogDemoTest
```


[C#]: https://en.wikipedia.org/wiki/C_Sharp_(programming_language)
[efcore.pg]: https://github.com/npgsql/efcore.pg
[Entity Framework Core]: https://learn.microsoft.com/en-gb/ef/core/
[Npgsql - .NET Access to PostgreSQL]: https://github.com/npgsql/npgsql
