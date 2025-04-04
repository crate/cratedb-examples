#######################
python-turbodbc backlog
#######################

Various items how this little code example can be improved.

- [x] Provide basic example
- [x] Insert multiple records using parameters
- [x] Docs: Add installation on SUSE
- [x] Provide example(s) for different operating systems (Linux, macOS)
- [x] Using turbodbc 4 is not an option, see https://github.com/blue-yonder/turbodbc/issues/437
- [x] Note turbodbc=5.0.1 should only require numpy>=2 in the build environment but should run also with e.g. numpy=1.26
- [x] Let's use NumPy 2 across the board
- [o] Docs: Drop a note about connecting with driver file vs. connecting via DSN
- [o] Evaluate different ODBC drivers
- [o] Provide an example scenario how to run it on Windows
- [o] Exercise advanced NumPy and PyArrow options
- [o] Exchange advanced CrateDB data types like ``OBJECT``, ``ARRAY``, and friends
- [o] Use ``SSLmode = Yes`` to connect to CrateDB Cloud
- [o] Explore other driver options at `Zabbix » Recommended UnixODBC settings for PostgreSQL`_
- [o] Check out https://github.com/dirkjonker/sqlalchemy-turbodbc
- [o] Check out https://docs.devart.com/odbc/postgresql/centos.htm


.. _Zabbix » Recommended UnixODBC settings for PostgreSQL: https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/odbc_checks/unixodbc_postgresql
