# CrateDB <-> Metabase backlog


## metabase/metabase:v0.45.4.3

```
2024-11-22 23:22:07,139 ERROR driver.util :: Failed to connect to Database
org.postgresql.util.PSQLException: The server does not support SSL.
```

```
2024-11-22 23:22:07,290 WARN metabase.email :: Failed to send email
clojure.lang.ExceptionInfo: SMTP host is not set. {:cause :smtp-host-not-set}
```

```
2024-11-22 23:22:08,189 WARN sync.util :: Error running step 'sync-timezone' for postgres Database 2 'cratedb-testdrive'
java.lang.Exception: Unable to parse date string '2024-11-22 23:22:08.175 ' for database engine 'postgres'
```

```
2024-11-22 23:22:08,724 WARN sync.describe-table :: Don't know how to map column type '_int4' to a Field base_type, falling back to :type/*.
2024-11-22 23:22:08,724 WARN sync.describe-table :: Don't know how to map column type '_int4' to a Field base_type, falling back to :type/*.
2024-11-22 23:22:08,725 WARN sync.describe-table :: Don't know how to map column type 'regclass' to a Field base_type, falling back to :type/*.
2024-11-22 23:22:08,725 WARN sync.describe-table :: Don't know how to map column type '_int4' to a Field base_type, falling back to :type/*.
2024-11-22 23:22:08,726 WARN sync.describe-table :: Don't know how to map column type '_int2' to a Field base_type, falling back to :type/*.
...
```

```
2024-11-22 23:22:13,900 WARN sync.util :: Error fingerprinting Table 12 'sys.jobs'
clojure.lang.ExceptionInfo: Error executing query: ERROR: line 2:359: no viable alternative at input 'SELECT "source"."substring531" AS "substring531", "source"."substring532" AS "substring532", "source"."substring533" AS "substring533", "source"."started" AS "started", "source"."substring534" AS "substring534", "source"."substring535" AS "substring535", "source"."substring536" AS "substring536" FROM (SELECT "sys"."jobs"."id" AS "id", ("sys"."jobs"."node"#>'
```

```
2024-11-22 23:22:14,390 WARN sync.util :: Error fingerprinting Table 13 'sys.nodes'
clojure.lang.ExceptionInfo: Error executing query: ERROR: line 2:97: no viable alternative at input 'SELECT "source"."load['probe_timestamp']" AS "load['probe_timestamp']", ("source"."fs['total']"#>'
```

```
2024-11-22 23:22:23,588 ERROR models.field-values :: Error fetching field values
clojure.lang.ExceptionInfo: Error executing query: ERROR: Cannot ORDER BY 'conffeqop': invalid data type 'integer_array'.

2024-11-22 23:22:23,599 ERROR models.field-values :: Error fetching field values
clojure.lang.ExceptionInfo: Error executing query: ERROR: Cannot ORDER BY 'conkey': invalid data type 'smallint_array'.
```
