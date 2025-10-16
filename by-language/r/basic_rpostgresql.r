# Install driver on demand.
# RPostgreSQL: R Interface to the 'PostgreSQL' Database System
# https://cran.r-project.org/web/packages/RPostgreSQL/

# Optionally install the PostgreSQL library.
if (!requireNamespace("RPostgreSQL", quietly = TRUE)) {
    install.packages("RPostgreSQL", repos="https://cran.r-project.org")
}

# Load the DBI and PostgreSQL libraries.
library(DBI)
library(RPostgreSQL)
drv <- RPostgreSQL::PostgreSQL()

# Open a database connection, where `dbname` is the name of the CrateDB schema.
conn <- dbConnect(drv,
                 host = "localhost",
                 port = 5432,
                 user = "crate",
                 password = "crate",
                 dbname = "doc",
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
res <- dbGetQuery(conn, "CREATE TABLE IF NOT EXISTS r (id INT PRIMARY KEY, data TEXT);")
res <- dbGetQuery(conn, "INSERT INTO r (id, data) VALUES (42, 'foobar');")
res <- dbGetQuery(conn, "REFRESH TABLE r;")
res <- dbGetQuery(conn, "SELECT * FROM r;")
print(res)
