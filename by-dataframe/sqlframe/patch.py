import json
import typing as t
from collections import OrderedDict

from sqlframe.base.session import _BaseSession
from sqlframe.postgres import PostgresCatalog, PostgresSession
from sqlglot import Generator, TokenType, exp
from sqlglot.dialects import Postgres


def monkeypatch():
    """
    Monkeypatch `sqlglot` and `sqlframe` until submitting a dedicated dialect for CrateDB.
    """
    Postgres.Tokenizer.KEYWORDS.update(
        {
            "GEO_POINT": TokenType.GEOGRAPHY,
            "GEO_SHAPE": TokenType.GEOGRAPHY,
        }
    )

    def var_map_sql(
        self: Generator,
        expression: t.Union[exp.Map, exp.VarMap],
        map_func_name: str = "MAP",
    ) -> str:
        """
        CrateDB accepts values for `OBJECT` types serialized as JSON.
        """
        keys = expression.args["keys"]
        values = expression.args["values"]
        data = OrderedDict()
        for key, value in zip(keys.expressions, values.expressions):
            data[str(key).strip("'")] = str(value).strip("'")
        return "'{}'".format(json.dumps(data))

    def cast_sql(
        self, expression: exp.Cast, safe_prefix: t.Optional[str] = None
    ) -> str:
        """
        Omit CASTing with CrateDB: Some values reflect as `TEXT`, which is wrong.

        TODO: REVIEW: Is it sane to do it this way?
              Can the type mapping be improved somehow?
        """
        format_sql = self.sql(expression, "format")
        format_sql = f" FORMAT {format_sql}" if format_sql else ""
        to_sql = self.sql(expression, "to")
        to_sql = f" {to_sql}" if to_sql else ""
        action = self.sql(expression, "action")
        action = f" {action}" if action else ""
        # Original:
        # return f"{safe_prefix or ''}CAST({self.sql(expression, 'this')} AS{to_sql}{format_sql}{action})"
        # CrateDB adjusted:
        return f"{self.sql(expression, 'this')}"

    Postgres.Generator.TRANSFORMS.update(
        {
            exp.Map: var_map_sql,
            exp.VarMap: var_map_sql,
        }
    )
    Generator.cast_sql = cast_sql
    PostgresCatalog.currentCatalog = lambda _: "crate"
    PostgresSession.__init__ = _BaseSession.__init__
