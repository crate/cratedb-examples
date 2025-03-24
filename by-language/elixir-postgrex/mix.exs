defmodule CrateDBExample.MixProject do
  use Mix.Project

  def project do
    [
      app: :cratedb_elixir_example,
      version: "0.0.0",
      elixir: "~> 1.0",
      deps: deps(),
    ]
  end

  def application() do
    []
  end

  defp deps() do
    [
      {:jason, "~> 1.4"},
      {:postgrex, "~> 0.20.0"},
    ]
  end

end
