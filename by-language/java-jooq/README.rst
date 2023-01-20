.. highlight:: sh

############################################################
Java jOOQ demo application for CrateDB using PostgreSQL JDBC
############################################################

*****
About
*****

A demo application using `CrateDB`_ with `jOOQ`_ and the `PostgreSQL
JDBC driver`_.

It is intended as a basic example to demonstrate what currently works, and as a
testing rig for eventually growing a full-fledged CrateDB dialect, or at least
making the code generator work. Contributions are welcome.


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

In some kind, jOOQ is similar to `LINQ`_, `but better <Insight into Language
Integrated Querying_>`_.


Details
=======

The code example will demonstrate a few of the `different use cases for jOOQ`_.
That is, `Dynamic SQL`_, the `jOOQ DSL API`_, and how to use `jOOQ as a SQL
builder without code generation`_.


Caveats
=======

- Most of the jOOQ examples use uppercase letters for the database, table, and
  field names. CrateDB currently only handles lowercase letters.


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


.. _CrateDB: https://github.com/crate/crate
.. _Different use cases for jOOQ: https://www.jooq.org/doc/latest/manual/getting-started/use-cases/
.. _Dynamic SQL: https://www.jooq.org/doc/latest/manual/sql-building/dynamic-sql/
.. _Gradle: https://gradle.org/
.. _Insight into Language Integrated Querying: https://blog.jooq.org/jooq-tuesdays-ming-yee-iu-gives-insight-into-language-integrated-querying/
.. _Java 17: https://adoptium.net/temurin/releases/?version=17
.. _jOOQ: https://github.com/jOOQ/jOOQ
.. _jOOQ as a SQL builder without code generation: https://www.jooq.org/doc/latest/manual/getting-started/use-cases/jooq-as-a-sql-builder-without-codegeneration/
.. _jOOQ's code generator: https://www.jooq.org/doc/latest/manual/code-generation/
.. _jOOQ DSL API: https://www.jooq.org/doc/latest/manual/sql-building/dsl-api/
.. _LINQ: https://en.wikipedia.org/wiki/Language_Integrated_Query
.. _PostgreSQL JDBC Driver: https://github.com/pgjdbc/pgjdbc
