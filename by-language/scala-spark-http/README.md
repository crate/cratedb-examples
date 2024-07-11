# Scala example loading data from Spark to CrateDB via http

This example aims to demostrate how a Spark data frame can be loaded into CrateDB using the CrateDB http endpoint.

It assumes there is a CrateDB instance running on localhost accepting connections with the default `crate` superuser, and it relies on the following table being created:

.. code-block:: sql

    CREATE TABLE myschema.mytable (
        examplefield1   TIMESTAMP,
        anotherfield    geo_point,
        jsonpayload     OBJECT
    );

In environments with very high volumes of data you may want to consider replacing scalaj.http with async calls with `akka.http` or `AsyncHttpClient`.
You may also want to explore if connection pooling is useful in your environment, and if JDBC calls leveraging the PostgreSQL wire protocol are more convenient for your particular case.

You can run this example with [sbt]:

.. code-block:: shell

    sbt run

[sbt]: https://www.scala-sbt.org/download/
