# CrateDB <-> Metabase backlog


## metabase/metabase:v0.48.4
Starts tripping with a hard error.
```
metabase  | 2024-11-23 16:34:33,843 WARN sync.util :: Error in sync step Sync postgres Database 2 'cratedb-testdrive'
metabase  | org.postgresql.util.PSQLException: ERROR: line 5:20: no viable alternative at input 'select\n   NULL as role,\n   t.schemaname as schema,\n   t.objectname as table'
```
```sql
with table_privileges as (
 select
   NULL as role,
   t.schemaname as schema,
   t.objectname as table,
   pg_catalog.has_table_privilege(current_user, '"' || t.schemaname || '"' || '.' || '"' || t.objectname || '"',  'UPDATE') as update,
   pg_catalog.has_table_privilege(current_user, '"' || t.schemaname || '"' || '.' || '"' || t.objectname || '"',  'SELECT') as select,
   pg_catalog.has_table_privilege(current_user, '"' || t.schemaname || '"' || '.' || '"' || t.objectname || '"',  'INSERT') as insert,
   pg_catalog.has_table_privilege(current_user, '"' || t.schemaname || '"' || '.' || '"' || t.objectname || '"',  'DELETE') as delete
 from (
   select schemaname, tablename as objectname from pg_catalog.pg_tables
   union
   select schemaname, viewname as objectname from pg_catalog.pg_views
   union
   select schemaname, matviewname as objectname from pg_catalog.pg_matviews
 ) t
 where t.schemaname !~ '^pg_'
   and t.schemaname <> 'information_schema'
   and pg_catalog.has_schema_privilege(current_user, t.schemaname, 'USAGE')
)
select t.*
from table_privileges t;
```
```
SQLParseException[line 5:17: no viable alternative at input 'select\nNULL as role,\nt.schemaname as schema,\nt.objectname as table']
```


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
