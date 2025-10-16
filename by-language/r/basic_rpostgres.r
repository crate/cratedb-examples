# Install driver on demand.
# RPostgres: C++ Interface to PostgreSQL
# https://cran.r-project.org/web/packages/RPostgres/

# Optionally install the PostgreSQL library.
if (!requireNamespace("RPostgres", quietly = TRUE)) {
    install.packages("RPostgres", repos="https://cran.r-project.org")
}

# Load the DBI and PostgreSQL libraries.
library(DBI)
library(RPostgres)
drv <- Postgres()

# Open a database connection, where `dbname` is the name of the CrateDB schema.
conn <- dbConnect(drv,
                  host = "localhost",
                  port = 5432,
                  user = "crate",
                  dbname = "testdrive",
                  )
on.exit(DBI::dbDisconnect(conn), add = TRUE)

# Invoke a basic select query.
res <- dbGetQuery(conn, "SELECT mountain, region, height FROM sys.summits ORDER BY HEIGHT DESC LIMIT 10;")
print(res)

# Delete testdrive table when needed.
# FIXME: https://github.com/crate/crate/issues/18528
#if (dbExistsTable(conn, "r")) {
#    dbRemoveTable(conn, "r")
#}

# Basic I/O.
res <- dbSendQuery(conn, "CREATE TABLE IF NOT EXISTS r (id INT PRIMARY KEY, data TEXT);")
dbClearResult(res)
# FIXME: Remove `ON CONFLICT DO NOTHING` after issue above got resolved.
res <- dbSendQuery(conn, "INSERT INTO r (id, data) VALUES (42, 'foobar') ON CONFLICT DO NOTHING;")
dbClearResult(res)
res <- dbSendQuery(conn, "REFRESH TABLE r;")
dbClearResult(res)
res <- dbGetQuery(conn, "SELECT * FROM r;")
print(res)
