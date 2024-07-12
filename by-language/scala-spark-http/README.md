# Scala example loading data from Spark to CrateDB via http

This example aims to demonstrate how a Spark data frame can be loaded into CrateDB using the CrateDB http endpoint.

It assumes there is a CrateDB instance running on localhost accepting connections with the default `crate` superuser, and it relies on the following table being created:

.. code-block:: sql

    CREATE TABLE myschema.mytable (
        examplefield1   TIMESTAMP,
        anotherfield    geo_point,
        jsonpayload     OBJECT
    );

When applicable for your environment, you may want to consider to replace `scalaj.http` with async calls like `akka.http` or `AsyncHttpClient`.
You may also want to explore if connection pooling is useful in your environment,
and if JDBC calls leveraging the PostgreSQL wire protocol are more convenient
for your particular case.

Saying this, note that this example uses [CrateDB's HTTP bulk operations] to ingest
data, which is currently the most efficient way to do it.

[CrateDB's HTTP bulk operations]: https://cratedb.com/docs/guide/performance/inserts/bulk.html

You can run this example with [sbt]:

.. code-block:: shell

    sbt run

[sbt]: https://www.scala-sbt.org/download/
