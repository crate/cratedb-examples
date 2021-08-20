##################################################
Basic example for connecting to CrateDB using JDBC
##################################################


*****
About
*****

This is a basic example program derived from `How can I connect to CrateDB using JDBC?`_.
It demonstrates CrateDB's `PostgreSQL wire protocol`_ compatibility by exercising a basic
example using both the vanilla `PgJDBC Driver`_ and the `CrateDB JDBC Driver`_.

For further information, please also visit the `CrateDB clients and tools`_ page.
Because CrateDB only supports (implicitly created) `table schemas`_ instead of databases,
it makes sense to also have a look at the `PostgreSQL documentation about schemas`_.


*****
Usage
*****

Run CrateDB::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate/crate:4.6.1

Create schema and insert data::

    psql postgres://crate@localhost:5432/doc

::

    crate=> CREATE TABLE testdrive (id INT PRIMARY KEY, data TEXT);
    CREATE 1
    crate=> INSERT INTO testdrive VALUES (0, 'zero'), (1, 'one'), (2, 'two');
    INSERT 0 3

Invoke example program::

    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/spikes/jdbc-basic

    # Use vanilla PgJDBC driver
    mvn install exec:java -Dexec.args="'jdbc:postgresql://localhost:5432/'"

    # Use CrateDB JDBC driver
    mvn install exec:java -Dexec.args="'jdbc:crate://localhost:5432/'"

In order to clean the build artefacts, invoke::

    mvn clean



.. _CrateDB clients and tools: https://crate.io/docs/crate/clients-tools/
.. _CrateDB JDBC Driver: https://github.com/crate/crate-jdbc
.. _How can I connect to CrateDB using JDBC?: https://community.crate.io/t/how-can-i-connect-to-cratedb-using-jdbc/400
.. _PostgreSQL documentation about schemas: https://www.postgresql.org/docs/current/ddl-schemas.html
.. _PostgreSQL wire protocol: https://crate.io/docs/reference/en/latest/protocols/postgres.html
.. _PgJDBC Driver: https://jdbc.postgresql.org/
.. _table schemas: https://crate.io/docs/crate/reference/en/4.6/general/ddl/create-table.html#schemas
