##################################################
Basic examples for connecting to CrateDB with Ruby
##################################################


*****
About
*****

This is a basic example program for connecting to CrateDB with Ruby.
It uses the `crate_ruby`_ driver to connect to CrateDB using HTTP.
It also demonstrates CrateDB's `PostgreSQL wire protocol`_ compatibility by
exercising the same example using Ruby's canonical `pg`_ driver.

For further information, please also visit the `CrateDB clients and tools`_ page.
Because CrateDB only supports (implicitly created) `table schemas`_ instead of databases,
it makes sense to also have a look at the `PostgreSQL documentation about schemas`_.


*****
Usage
*****

Run CrateDB::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:5.1.1

Install example program::

    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/by-language/ruby

    gem install bundler
    bundle install

Invoke example program::

    # Using `crate_ruby` driver.
    ruby ruby_example.rb crate_ruby

    # Using `pg` driver.
    ruby ruby_example.rb pg


.. _CrateDB clients and tools: https://crate.io/docs/crate/clients-tools/
.. _crate_ruby: https://github.com/crate/crate_ruby
.. _pg: https://rubygems.org/gems/pg
.. _PostgreSQL documentation about schemas: https://www.postgresql.org/docs/current/ddl-schemas.html
.. _PostgreSQL wire protocol: https://crate.io/docs/reference/en/latest/protocols/postgres.html
.. _table schemas: https://crate.io/docs/crate/reference/en/latest/general/ddl/create-table.html#schemas
