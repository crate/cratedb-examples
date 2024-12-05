.. highlight: console

####################################################################
Basic example for connecting to CrateDB and CrateDB Cloud using JDBC
####################################################################


*****
About
*****

This is a basic example program derived from `How can I connect to CrateDB using JDBC?`_.
It demonstrates CrateDB's `PostgreSQL wire protocol`_ compatibility by exercising a basic
example using both the vanilla `PostgreSQL JDBC Driver`_ and the `CrateDB legacy JDBC driver`_.

For further information, please also visit the `CrateDB clients and tools`_ page.
Because CrateDB only supports (implicitly created) `table schemas`_ instead of databases,
it makes sense to also have a look at the `PostgreSQL documentation about schemas`_.


*****
Usage
*****

To start a CrateDB instance on your machine for evaluation purposes, invoke::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate

Invoke example program::

    # Acquire sources.
    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/by-language/java-jdbc

    # Download dependencies and build program.
    mvn install

    # Display program options.
    mvn exec:java -Dexec.args="--help"

Connect to instance on ``localhost``::

    # Use vanilla PostgreSQL JDBC driver.
    mvn exec:java -Dexec.args="--dburl 'jdbc:postgresql://localhost:5432/testdrive'"

    # Use CrateDB legacy JDBC driver.
    mvn exec:java -Dexec.args="--dburl 'jdbc:crate://localhost:5432/testdrive'"

Connect to CrateDB Cloud::

    # Use vanilla PostgreSQL JDBC driver.
    mvn exec:java -Dexec.args="--dburl 'jdbc:postgresql://example.aks1.westeurope.azure.cratedb.net:5432/testdrive' --user 'admin' --password '<PASSWORD>'"

    # Use CrateDB legacy JDBC driver.
    mvn exec:java -Dexec.args="--dburl 'jdbc:crate://example.aks1.westeurope.azure.cratedb.net:5432/testdrive' --user 'admin' --password '<PASSWORD>'"

In order to clean the build artefacts, invoke::

    mvn clean


.. _CrateDB clients and tools: https://crate.io/docs/crate/clients-tools/
.. _CrateDB legacy JDBC driver: https://github.com/crate/crate-jdbc
.. _How can I connect to CrateDB using JDBC?: https://community.crate.io/t/how-can-i-connect-to-cratedb-using-jdbc/400
.. _PostgreSQL documentation about schemas: https://www.postgresql.org/docs/current/ddl-schemas.html
.. _PostgreSQL JDBC Driver: https://jdbc.postgresql.org/
.. _PostgreSQL wire protocol: https://crate.io/docs/reference/en/latest/protocols/postgres.html
.. _table schemas: https://crate.io/docs/crate/reference/en/4.6/general/ddl/create-table.html#schemas
