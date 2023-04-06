/**
 * An example application for demonstrating "Testcontainers for Java" with CrateDB and the PostgreSQL JDBC driver.
 *
 * - https://github.com/crate/crate
 * - https://github.com/testcontainers/testcontainers-java
 * - https://www.testcontainers.org/modules/databases/cratedb/
 * - https://github.com/pgjdbc/pgjdbc
 */

package io.crate.example.testing;

import java.io.IOException;
import java.sql.*;
import java.util.Locale;
import java.util.Properties;

public class Application {

    public String dsn;
    public String user;

    public Application(String connectionUrl) {
        dsn = connectionUrl;
        user = "crate";
    }

    public Application(String connectionUrl, String userName) {
        dsn = connectionUrl;
        user = userName;
    }

    public static void main(String[] args) throws IOException, SQLException {
        if (args.length != 1) {
            throw new IOException(
                    "ERROR: Need a single argument, the database connection URL.\n\n" +
                    "Examples:\n" +
                    "./gradlew run --args=\"jdbc:crate://localhost:5432/\"\n" +
                    "./gradlew run --args=\"jdbc:postgresql://localhost:5432/\"\n");
        }
        String connectionUrl = args[0];
        Application app = new Application(connectionUrl);
        app.querySummitsTable();
        System.out.println("Ready.");
    }

    /**
     * Example database conversation: Query the built-in `sys.summits` table of CrateDB.
     */
    public void querySummitsTable() throws IOException, SQLException {
        this.query("SELECT * FROM sys.summits LIMIT 3;");
    }

    public void query(String sql) throws IOException, SQLException {

        Properties connectionProps = new Properties();
        connectionProps.put("user", user);

        Connection sqlConnection = DriverManager.getConnection(dsn, connectionProps);
        sqlConnection.setAutoCommit(true);
        if (sqlConnection.isClosed()) {
            throw new IOException("ERROR: Unable to open connection to database");
        }
        try (Statement stmt = sqlConnection.createStatement()) {
            boolean checkResults = stmt.execute(sql);
            if (checkResults) {
                ResultSet rs = stmt.getResultSet();
                while (rs.next()) {
                    System.out.printf(Locale.ENGLISH, "> row %d\n", rs.getRow());
                    ResultSetMetaData metaData = rs.getMetaData();
                    int columnCount = metaData.getColumnCount();
                    for (int i = 1; i <= columnCount; i++) {
                        System.out.printf(
                                Locale.ENGLISH,
                                ">> col %d: %s: %s\n",
                                i,
                                metaData.getColumnName(i),
                                rs.getObject(i));
                    }
                }
            } else {
                throw new IOException("ERROR: Result is empty");
            }
        }
        sqlConnection.close();

    }

}
