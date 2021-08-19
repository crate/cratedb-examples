##################################################
Basic example for connecting to CrateDB using JDBC
##################################################


*****
About
*****

This is a basic example program derived from `How can I connect to CrateDB using JDBC?`_.
It demonstrates CrateDB's `PostgreSQL wire protocol`_ compatibility by exercising a basic
example using both the vanilla `PgJDBC Driver`_ and the `CrateDB JDBC Driver`_.

For CrateDB version 4.2 and higher, we recommend to use the vanilla driver.


*****
Usage
*****

Run CrateDB::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate/crate:4.6.1

Create schema and insert data::

    psql postgres://crate@localhost:5432/

::

    crate=> CREATE TABLE testdrive (id INT PRIMARY KEY, data TEXT);
    CREATE 1
    crate=> INSERT INTO testdrive VALUES (0, 'zero'), (1, 'one'), (2, 'two');
    INSERT 0 3

Invoke example program::

    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/spikes/jdbc-basic

    # Use vanilla PgJDBC driver
    mvn --debug install exec:java -Dexec.args="'jdbc:postgresql://localhost:5432/'"

    # Use CrateDB JDBC driver
    mvn --debug install exec:java -Dexec.args="'jdbc:crate://localhost:5432/'"

In order to clean the build artefacts, invoke::

    mvn clean



.. _CrateDB JDBC Driver: https://github.com/crate/crate-jdbc
.. _PostgreSQL wire protocol: https://crate.io/docs/reference/en/latest/protocols/postgres.html
.. _PgJDBC Driver: https://jdbc.postgresql.org/
.. _How can I connect to CrateDB using JDBC?: https://community.crate.io/t/how-can-i-connect-to-cratedb-using-jdbc/400
