################
CrateDB Examples
################


*****
About
*****

A collection of clear and concise examples how to work with `CrateDB`_.
You can use them as blueprints for your own projects.


******
Layout
******

- The ``by-language`` folder contains demo programs / technical investigations
  outlining how to get started quickly with CrateDB using different programming
  languages and frameworks.

- The ``queries`` folder contains different SQL query examples for typical use
  cases in order to explain specific features of CrateDB.

- The ``stacks`` folder contains more grown-up, complete usage scenarios where
  CrateDB is part of a larger software stack. Those resources may also be used
  within "reference architecture" types of documentation.

- The ``testing`` folder contains reference implementations about how to use
  different kinds of test layers for testing your applications with CrateDB.


*******
Testing
*******

The repository includes an universal test runner, which can be used to invoke
test suites of different languages and environments.

Examples::

    python testing/ngr.py by-language/csharp-npgsql
    python testing/ngr.py by-language/csharp-npgsql --npgsql-version=6.0.9
    python testing/ngr.py by-language/php-amphp
    python testing/ngr.py by-language/php-pdo
    python testing/ngr.py by-language/python-sqlalchemy
    python testing/ngr.py by-language/ruby

It is recommended to invoke ``ngr`` from within a Python virtualenv.

.. _CrateDB: https://github.com/crate/crate
