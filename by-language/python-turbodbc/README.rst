###########################
Using CrateDB with turbodbc
###########################


*****
About
*****

This section of the documentation describes how to connect to `CrateDB`_
with `turbodbc`_, by providing a few example programs.

The examples use the `unixODBC`_ implementation of `ODBC`_, and the `PostgreSQL
ODBC driver`_, for connecting to the `PostgreSQL wire protocol`_ interface of
`CrateDB`_.

This folder also contains ``Dockerfile`` files providing environments to
exercise the examples on different operating systems, like Arch Linux,
Red Hat (CentOS), Debian, and SUSE Linux.


************
Introduction
************

`Turbodbc`_ is a Python module to access relational databases via the `Open
Database Connectivity (ODBC)`_ interface. In addition to complying with
the `Python Database API Specification 2.0`_, turbodbc offers built-in `NumPy`_
and `Apache Arrow`_ support for improved performance. Their slogan is:

    Don’t wait minutes for your results, just blink.

*Note: The description texts have been taken from turbodbc's documentation 1:1.*

Description
===========

Its primary target audience are data scientists that use databases for which no
efficient native Python drivers are available.

For maximum compatibility, turbodbc complies with the `Python Database API
Specification 2.0`_ (PEP 249). For maximum performance, turbodbc internally
relies on batched data transfer instead of single-record communication as
other popular ODBC modules do.

Why should I use turbodbc instead of other ODBC modules?
========================================================

- Short answer: turbodbc is faster.
- Slightly longer answer: turbodbc is faster, *much* faster if you want to
  work with NumPy.
- Medium-length answer: The author has tested turbodbc and pyodbc (probably
  the most popular Python ODBC module) with various databases (Exasol,
  PostgreSQL, MySQL) and corresponding ODBC drivers. He found turbodbc to be
  consistently faster.

Smooth. What is the trick?
==========================

Turbodbc exploits buffering.

- Turbodbc implements both sending parameters and retrieving result sets using
  buffers of multiple rows/parameter sets. This avoids round trips to the ODBC
  driver and (depending how well the ODBC driver is written) to the database.
- Multiple buffers are used for asynchronous I/O. This allows to interleave
  Python object conversion and direct database interaction (see performance
  options below).
- Buffers contain binary representations of data. NumPy arrays contain binary
  representations of data. Good thing they are often the same, so instead of
  converting, the driver can just copy data.


*****
Setup
*****

Install prerequisites
=====================

Arch Linux::

    # See `dockerfiles/archlinux.Dockerfile`.

CentOS Stream::

    dnf install --enablerepo=crb -y boost-devel g++ postgresql-odbc python3 python3-devel python3-pip unixODBC-devel

Debian::

    apt-get install --yes build-essential libboost-dev odbc-postgresql unixodbc-dev

macOS/Homebrew::

    brew install psqlodbc unixodbc

SUSE Linux Enterprise Server::

    # See `dockerfiles/sles.Dockerfile`.

Install Python sandbox
======================
::

    # Create Python virtualenv and install dependency packages.
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade --requirement=requirements-prereq.txt
    pip install --upgrade --requirement=requirements.txt --verbose

.. note::

    The `turbodbc pip installation documentation`_ says:
    Please ``pip install numpy`` before installing turbodbc, because turbodbc
    will search for the ``numpy`` Python package at installation/compile time.
    If NumPy is not installed, turbodbc will not compile the `NumPy
    support`_ features. Similarly, please ``pip install pyarrow`` before
    installing turbodbc if you would like to use the `Apache Arrow
    support`_.


*****
Usage
*****

Run CrateDB::

    docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate \
        -Cdiscovery.type=single-node -Ccluster.routing.allocation.disk.threshold_enabled=false

Invoke demo program on workstation::

	python demo.py

Exercise demo program using Docker, on different operating systems::

    docker build --progress=plain --tag local/python-turbodbc-demo --file=dockerfiles/archlinux.Dockerfile .
    docker build --progress=plain --tag local/python-turbodbc-demo --file=dockerfiles/centos.Dockerfile .
    docker build --progress=plain --tag local/python-turbodbc-demo --file=dockerfiles/debian.Dockerfile .
    docker build --progress=plain --tag local/python-turbodbc-demo --file=dockerfiles/sles.Dockerfile .

    docker run --rm -it --volume=$(pwd):/src --network=host local/python-turbodbc-demo python3 /src/demo.py


*******
Backlog
*******

The patch just contains a basic example within ``demo.py``. Advanced usage
examples to be exercised are tracked within the `backlog`_.



.. _Apache Arrow: https://en.wikipedia.org/wiki/Apache_Arrow
.. _Apache Arrow support: https://turbodbc.readthedocs.io/en/latest/pages/advanced_usage.html#advanced-usage-arrow
.. _backlog: https://github.com/crate/cratedb-examples/blob/main/python-turbodbc/backlog.rst
.. _CrateDB: https://github.com/crate/crate
.. _NumPy: https://en.wikipedia.org/wiki/NumPy
.. _NumPy support: https://turbodbc.readthedocs.io/en/latest/pages/advanced_usage.html#advanced-usage-numpy
.. _ODBC: https://en.wikipedia.org/wiki/Open_Database_Connectivity
.. _Open Database Connectivity (ODBC): https://en.wikipedia.org/wiki/Open_Database_Connectivity
.. _PostgreSQL ODBC driver: https://odbc.postgresql.org/
.. _PostgreSQL wire protocol: https://crate.io/docs/crate/reference/en/latest/interfaces/postgres.html
.. _Python Database API Specification 2.0: https://peps.python.org/pep-0249/
.. _turbodbc: https://turbodbc.readthedocs.io/
.. _turbodbc pip installation documentation: https://turbodbc.readthedocs.io/en/latest/pages/getting_started.html#pip
.. _unixODBC: https://www.unixodbc.org/
