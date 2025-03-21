# Install driver on demand.
# RPostgreSQL: R Interface to the 'PostgreSQL' Database System
# https://cran.r-project.org/web/packages/RPostgreSQL/
if (!require(RPostgreSQL)) {
    install.packages("RPostgreSQL", repos="http://cran.us.r-project.org")
}
stopifnot(require(RPostgreSQL))

# Load the DBI library.
library(DBI)
drv <- dbDriver("PostgreSQL")

# Open a database connection, where `dbname` is the name of the CrateDB schema.
con <- dbConnect(drv,
                 host = "localhost",
                 port = 5432,
                 user = "crate",
                 dbname = "testdrive",
                 )

# Invoke a basic select query.
res <- dbGetQuery(con, "SELECT mountain, region, height FROM sys.summits ORDER BY HEIGHT DESC LIMIT 10;")
print(res)

# Delete testdrive table when needed.
if (dbExistsTable(con, "r")) {
    dbRemoveTable(con, "r")
}

# Basic I/O.
res <- dbGetQuery(con, "CREATE TABLE IF NOT EXISTS r (id INT PRIMARY KEY, data TEXT);")
res <- dbGetQuery(con, "INSERT INTO r (id, data) VALUES (42, 'foobar');")
res <- dbGetQuery(con, "REFRESH TABLE r;")
res <- dbGetQuery(con, "SELECT * FROM r;")
print(res)
