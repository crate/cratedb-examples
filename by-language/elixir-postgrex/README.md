# Connecting to CrateDB with Elixir

## About

The file `test/basic_test.exs` includes a basic example program that uses
the canonical PostgreSQL driver for Elixir, [Postgrex], to connect to
CrateDB.

## Usage

Start a CrateDB instance for evaluation purposes.
```shell
docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest
```

Invoke example program.
```shell
mix deps.get
mix test --trace
```

## Trivia

This folder contains a minimal Elixir project using [Hex] and [Mix]
for package management, and [ExUnit] for unit testing.

[Hex] is [Elixir]'s package manager.

> [Elixir] ships with a great set of tools to ease development. [Mix] is a
> build tool that allows you to easily create projects, manage tasks,
> run tests and more.
>
> [Mix] also integrates with the [Hex] package manager for dependency management
> and hosting documentation for the whole ecosystem.
>
> -- https://elixir-lang.org/


[Elixir]: https://elixir-lang.org/
[ExUnit]: https://hexdocs.pm/ex_unit/
[Hex]: https://hex.pm/
[Mix]: https://hexdocs.pm/mix/Mix.html
[Postgrex]: https://hexdocs.pm/postgrex/
