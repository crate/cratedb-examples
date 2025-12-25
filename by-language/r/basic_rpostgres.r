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
                  sslmode = "disable",
                  user = "crate",
                  password = "crate",
                  )
on.exit(DBI::dbDisconnect(conn), add = TRUE)

# Invoke a basic select query.
res <- dbGetQuery(conn, "SELECT mountain, region, height FROM sys.summits ORDER BY height DESC LIMIT 10;")
print(res)

# Delete testdrive table when needed.
if (dbExistsTable(conn, "r")) {
    dbRemoveTable(conn, "r")
}

# Basic I/O.
res <- dbSendQuery(conn, "CREATE TABLE r (id INT PRIMARY KEY, data TEXT);")
dbClearResult(res)
res <- dbSendQuery(conn, "INSERT INTO r (id, data) VALUES (42, 'foobar');")
dbClearResult(res)
res <- dbSendQuery(conn, "REFRESH TABLE r;")
dbClearResult(res)
res <- dbGetQuery(conn, "SELECT * FROM r;")
print(res)
