.. highlight: console

##############################################################
Connect to CrateDB and CrateDB Cloud using PHP PDO (PDO_PGSQL)
##############################################################


*****
About
*****

This is an example program demonstrating CrateDB's `PostgreSQL wire protocol`_
compatibility by exercising a few basic SQL statements using PHP's PDO database
adapter interface, see `PHP Data Objects`_. Specifically, it uses the `PDO_PGSQL`_
driver.

For further information, please also visit the `CrateDB clients and tools`_
page. Because CrateDB only supports (implicitly created) `table schemas`_
instead of databases, please also read `PostgreSQL documentation about
schemas`_ carefully.

Also, please note that support for this driver is experimental. The `CrateDB
PDO driver`_ is the official CrateDB PHP client supported by Crate.io.


*****
Usage
*****

To start a CrateDB instance on your machine for evaluation purposes, invoke::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate

Navigate to PDO example programs::

    # Acquire sources.
    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/by-language/php-pdo

Run basic example program, using vanilla PHP PDO_PGSQL driver::

    # Connect to CrateDB on localhost.
    php basic.php 'pgsql:host=localhost;port=5432;user=crate'

    # Connect to CrateDB Cloud.
    php basic.php 'pgsql:host=example.aks1.eastus2.azure.cratedb.net;port=5432;user=admin;password=<PASSWORD>'


.. _CrateDB clients and tools: https://crate.io/docs/crate/clients-tools/
.. _CrateDB PDO driver: https://crate.io/docs/pdo/
.. _PDO_PGSQL: https://www.php.net/manual/en/ref.pdo-pgsql.php
.. _PHP Data Objects: https://www.php.net/manual/en/book.pdo.php
.. _PostgreSQL documentation about schemas: https://www.postgresql.org/docs/current/ddl-schemas.html
.. _PostgreSQL wire protocol: https://crate.io/docs/reference/en/latest/protocols/postgres.html
.. _table schemas: https://crate.io/docs/crate/reference/en/latest/general/ddl/create-table.html#schemas
