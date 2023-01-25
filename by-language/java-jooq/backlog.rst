###################################################
Backlog for Java jOOQ demo application with CrateDB
###################################################


Features
========

- Evaluate more features of jOOQ, like:

  - `Using JDBC batch operations`_
  - `jOOQ for PROs`_, specifically but not exclusively `exporting`_ and `importing`_
  - `Alternative execution models`_
  - `The static query DSL API`_
  - `Configuration and setup of the generator`_

- jOOQ's code generator does not know about CrateDB's special data types.
  Evaluate if this will work when using the dynamic access variant, without
  using code generation. Of course, the container data types ``OBJECT`` and
  ``ARRAY`` are the most interesting ones.


Q & A
=====

- Question: Out of curiosity, validate if, under the hood, the actual
  abstraction layer is indeed ``org.hibernate.dialect.PostgreSQL94Dialect``?
  Answer: Yes, as of jOOQ 3.17.7, this is correct, see
  `org.jooq.SQLDialect#L1367-L1368`_.

- Question: How to set the default schema name? The ``unqualifiedSchema``
  property in ``jooq.gradle`` apparently only accepts ``public`` or ``none``.
  Answer: Please check the other ``jooq.gradle`` in branch
  ``amo/jooq/codegen``, see `jooq.gradle#L70-L73`_::

    database {
      name = 'org.jooq.meta.postgres.PostgresDatabase'
      inputSchema = 'testdrive'
    }


Other topics
============

- When jOOQ connects to CrateDB, it displays ``SET SESSION STATEMENT WILL BE
  IGNORED: extra_float_digits`` on the server console.

- Demonstrate usage together with `HikariCP`_, a high-performance JDBC
  connection pool.

- Discussion: Would it be sensible to get CrateDB into the `List of RDBMS
  supported by jOOQ`_, and what would it take?


Caveats
=======

The `README`_ lists multiple items in the "Caveats" section. Address them, when
possible.

- `Code generation with reflection from the database`_ has been evaluated, but
  does not work yet. The corresponding blockers are, at least, `support for
  "WITH RECURSIVE" CTEs`_, and `IllegalStateException on nested JOINs`_.
  The first ones happens when jOOQ issues a reflection query using the
  ``org.jooq.meta.postgres.PostgresDatabase`` code generator, and the second
  one happens when using the ``org.jooq.meta.jdbc.JDBCDatabase`` generator.



.. _Alternative execution models: https://www.jooq.org/doc/latest/manual/sql-execution/alternative-execution-models/
.. _code generation with reflection from the database: https://github.com/crate/cratedb-examples/pull/10
.. _Configuration and setup of the generator: https://www.jooq.org/doc/latest/manual/code-generation/codegen-configuration/
.. _exporting: https://www.jooq.org/doc/latest/manual/sql-execution/exporting/
.. _HikariCP: https://github.com/brettwooldridge/HikariCP
.. _IllegalStateException on nested JOINs: https://github.com/crate/crate/issues/13503
.. _importing: https://www.jooq.org/doc/latest/manual/sql-execution/importing/
.. _jOOQ for PROs: https://www.jooq.org/doc/latest/manual/getting-started/use-cases/jooq-for-pros/
.. _jooq.gradle#L70-L73: https://github.com/crate/cratedb-examples/blob/f88eda5/by-language/java-jooq/jooq.gradle#L70-L73
.. _List of RDBMS supported by jOOQ: https://www.jooq.org/doc/latest/manual/reference/supported-rdbms/
.. _org.jooq.SQLDialect#L1367-L1368: https://github.com/jOOQ/jOOQ/blob/version-3.17.7/jOOQ/src/main/java/org/jooq/SQLDialect.java#L1367-L1368
.. _README: README.rst
.. _Support for "WITH RECURSIVE" CTEs: https://github.com/crate/crate/issues/12544
.. _The static query DSL API: https://www.jooq.org/doc/latest/manual/sql-building/dsl/
.. _Using JDBC batch operations: https://www.jooq.org/doc/latest/manual/sql-execution/batch-execution/
