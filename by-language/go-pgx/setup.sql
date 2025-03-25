-- dbext:type=CRATE:host=localhost:port=4200:dbname=doc

CREATE TABLE IF NOT EXISTS testdrive.go_users (
  id LONG,
  name STRING,
  value FLOAT
)
