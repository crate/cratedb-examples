# https://hexdocs.pm/ex_unit/ExUnit.html#module-integration-with-mix
ExUnit.start()

defmodule Postgrex.TestHelper do
  defmacro query(stat, params, opts \\ []) do
    quote do
      case Postgrex.query(var!(context)[:pid], unquote(stat), unquote(params), unquote(opts)) do
        {:ok, %Postgrex.Result{rows: nil}} -> :ok
        {:ok, %Postgrex.Result{rows: rows}} -> rows
        {:error, err} -> err
      end
    end
  end

  defmacro prepare(name, stat, opts \\ []) do
    quote do
      case Postgrex.prepare(var!(context)[:pid], unquote(name), unquote(stat), unquote(opts)) do
        {:ok, %Postgrex.Query{} = query} -> query
        {:error, err} -> err
      end
    end
  end

  defmacro prepare_execute(name, stat, params, opts \\ []) do
    quote do
      case Postgrex.prepare_execute(
             var!(context)[:pid],
             unquote(name),
             unquote(stat),
             unquote(params),
             unquote(opts)
           ) do
        {:ok, %Postgrex.Query{} = query, %Postgrex.Result{rows: rows}} -> {query, rows}
        {:error, err} -> err
      end
    end
  end

  defmacro execute(query, params, opts \\ []) do
    quote do
      case Postgrex.execute(var!(context)[:pid], unquote(query), unquote(params), unquote(opts)) do
        {:ok, %Postgrex.Query{}, %Postgrex.Result{rows: nil}} -> :ok
        {:ok, %Postgrex.Query{}, %Postgrex.Result{rows: rows}} -> rows
        {:error, err} -> err
      end
    end
  end

  defmacro stream(query, params, opts \\ []) do
    quote do
      Postgrex.stream(var!(conn), unquote(query), unquote(params), unquote(opts))
    end
  end

  defmacro close(query, opts \\ []) do
    quote do
      case Postgrex.close(var!(context)[:pid], unquote(query), unquote(opts)) do
        :ok -> :ok
        {:error, err} -> err
      end
    end
  end

  defmacro transaction(fun, opts \\ []) do
    quote do
      Postgrex.transaction(var!(context)[:pid], unquote(fun), unquote(opts))
    end
  end
end
