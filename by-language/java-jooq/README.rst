.. highlight:: sh

#############################################################
Java jOOQ demo application with CrateDB using PostgreSQL JDBC
#############################################################


*****
About
*****

In a nutshell
=============

A demo application using `CrateDB`_ with `jOOQ`_ and the `PostgreSQL JDBC
driver`_. It uses the `Gradle Build Tool`_ and the `Gradle plugin for jOOQ code
generation`_.

It is intended as a basic example to demonstrate what currently works, and as a
testing rig for eventually growing a full-fledged CrateDB extension.
Contributions are welcome.

Introduction
============

The idea of jOOQ is to generate typesafe code based on the SQL schema.
Then, accessing a database table using the jOOQ DSL API looks like this:

.. code-block:: java

    // Fetch records, with filtering and sorting.
    Result<Record> result = db.select()
            .from(AUTHOR)
            .where(AUTHOR.NAME.like("Ja%"))
            .orderBy(AUTHOR.NAME)
            .fetch();

    // Iterate and display records.
    for (Record record : result) {
        Integer id = record.getValue(AUTHOR.ID);
        String name = record.getValue(AUTHOR.NAME);
        System.out.println("id: " + id + ", name: " + name);
    }


*******
Details
*******

Overview
========

The code examples will demonstrate a few of the `different use cases for jOOQ`_.
That is, how to use the `jOOQ DSL API`_ based on code generated with `jOOQ's
code generator`_ to take your database schema and reverse-engineer it into a
set of Java classes, as well how to use the `Dynamic SQL API`_ by using `jOOQ
as a SQL builder without code generation`_.

Schema management
=================

In many cases, the schema is defined in the form of SQL scripts, which can be
used with a `database schema migration`_ framework like `Flyway`_,
`Liquibase`_, `Bytebase`_, etc.

The `DDLDatabase - Code generation from SQL files`_ feature can be used to
effectively reflect the database schema from SQL DDL files, without needing
a database instance at all. The code provided within the ``src/generated``
directory has been generated like this.

Caveats
=======

Contributions to resolve any of those items will be welcome, see also
`backlog`_.

- `jOOQ's code generator`_ currently does not work with directly connecting to
  a real CrateDB database instance and reflecting the schema from there.
  With corresponding improvements to CrateDB, this can be made work in the
  future, see `issue #10 - with reflection from the database`_. Right now, this
  example uses code generation based on SQL DDL files, which is also supported
  by jOOQ.

- Applying code generation based on the database schema (directly, or via SQL
  DDL) is only supported for schema definitions which use field types
  compatible with standard PostgreSQL, and understood by jOOQ. jOOQ does not
  know anything about any other special data types supported by CrateDB, and
  does not support it. When using special field types, like ``IP``, it will
  trip the code generator.

- Most of the jOOQ examples use uppercase letters for the database, table, and
  field names. Within this setup, we have only been able to make it work using
  lowercase letters.

- We have not been able to make multiple SQL DDL statements work within a
  single SQL bootstrap file at ``src/main/resources/bootstrap.sql``.


*****
Usage
*****

1. Make sure `Java 17`_ is installed.
2. Run CrateDB::

       docker run -it --rm --publish=4200:4200 --publish=5432:5432 \
           crate:latest -Cdiscovery.type=single-node

3. Invoke demo application::

    ./gradlew run

3. Invoke software tests::

    ./gradlew test

4. Generate the jOOQ sources from the main jOOQ configuration, see ``jooq.gradle``::

    ./gradlew generateJooq


.. _backlog: backlog
.. _Bytebase: https://github.com/bytebase/bytebase
.. _CrateDB: https://github.com/crate/crate
.. _database schema migration: https://en.wikipedia.org/wiki/Schema_migration
.. _DDLDatabase - Code generation from SQL files: https://www.jooq.org/doc/latest/manual/code-generation/codegen-ddl/
.. _Different use cases for jOOQ: https://www.jooq.org/doc/latest/manual/getting-started/use-cases/
.. _Dynamic SQL API: https://www.jooq.org/doc/latest/manual/sql-building/dynamic-sql/
.. _Flyway: https://github.com/flyway/flyway
.. _Gradle Build Tool: https://gradle.org/
.. _Gradle plugin for jOOQ code generation: https://github.com/etiennestuder/gradle-jooq-plugin
.. _issue #10 - with reflection from the database: https://github.com/crate/cratedb-examples/pull/10
.. _Java 17: https://adoptium.net/temurin/releases/?version=17
.. _jOOQ: https://github.com/jOOQ/jOOQ
.. _jOOQ as a SQL builder without code generation: https://www.jooq.org/doc/latest/manual/getting-started/use-cases/jooq-as-a-sql-builder-without-codegeneration/
.. _jOOQ's code generator: https://www.jooq.org/doc/latest/manual/code-generation/
.. _jOOQ DSL API: https://www.jooq.org/doc/latest/manual/sql-building/dsl-api/
.. _Liquibase: https://github.com/liquibase/liquibase
.. _PostgreSQL JDBC Driver: https://github.com/pgjdbc/pgjdbc
