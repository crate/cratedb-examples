# https://hexdocs.pm/ex_unit/ExUnit.html

defmodule CrateDBTest do
  use ExUnit.Case, async: true
  alias Postgrex, as: P

  setup context do
    opts = [
      hostname: "localhost",
      username: "crate",
      password: "",
      database: "",
      backoff_type: :stop,
      prepare: context[:prepare] || :named,
      max_restarts: 0
    ]
    {:ok, pid} = P.start_link(opts)
    {:ok, _} = P.query(pid, "
        DROP TABLE IF EXISTS testdrive.elixir;
        ", [])
    {:ok, [pid: pid, options: opts]}

  end

  test "select sys.summits", context do
    {:ok, result} = P.query(var!(context)[:pid], "
        SELECT country, mountain, height, coordinates
        FROM sys.summits
        ORDER BY height DESC LIMIT 1;
        ", [])
    assert [["FR/IT", "Mont Blanc", 4808, %Postgrex.Point{x: 6.86444, y: 45.8325}]] == result.rows
  end

  test "object i/o", context do

    # DDL
    {:ok, _} = P.query(var!(context)[:pid], "
        CREATE TABLE testdrive.elixir (
            id INTEGER,
            data OBJECT(DYNAMIC)
        );
        ", [])

    # DML
    record = [42, %{"age" => 44, "name" => "Steve Irwin", "nationality" => "Australian"}]
    {:ok, _} = P.query(var!(context)[:pid], "
        INSERT INTO testdrive.elixir (id, data) VALUES (?, ?);
        ", record)
    {:ok, _} = P.query(var!(context)[:pid], "
        REFRESH TABLE testdrive.elixir;
        ", [])

    # DQL
    {:ok, result} = P.query(var!(context)[:pid], "
        SELECT *
        FROM testdrive.elixir;
        ", [])
    assert [[42, %{"age" => 44, "name" => "Steve Irwin", "nationality" => "Australian"}]] == result.rows

  end

  test "vector i/o", context do

    # DDL
    {:ok, _} = P.query(var!(context)[:pid], "
        CREATE TABLE testdrive.elixir (
            id INTEGER,
            data FLOAT_VECTOR(3)
        );
        ", [])

    # DML
    records = [
        [42, [0.1, 0.2, 0.3]],
        [43, [0.9, 0.3, 0.1]],
        [44, [0.5, 0.1, 0.8]],
        [45, [0.3, 0.9, 0.1]],
    ]
    for {record, _} <- Enum.with_index(records) do
        {:ok, _} = P.query(var!(context)[:pid], "
            INSERT INTO testdrive.elixir (id, data) VALUES (?, ?);
            ", record)
    end
    {:ok, _} = P.query(var!(context)[:pid], "
        REFRESH TABLE testdrive.elixir;
        ", [])

    # DQL
    {:ok, result} = P.query(var!(context)[:pid], "
        SELECT id
        FROM testdrive.elixir
        WHERE knn_match(data, ?, 2)
        ORDER BY id;
        ", [[0.1, 0.2, 0.3]])
    assert [~c"*", ~c"+", ~c",", ~c"-"] == result.rows

  end

end
