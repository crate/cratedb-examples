/**
 * An example application for demonstrating "Testcontainers for Java" with CrateDB and the PostgreSQL JDBC driver.
 * <ul>
 *  <li><a href="https://github.com/crate/crate"/></li>
 *  <li><a href="https://github.com/testcontainers/testcontainers-java"/></li>
 *  <li><a href="https://www.testcontainers.org/modules/databases/cratedb/"/></li>
 *  <li><a href="https://github.com/pgjdbc/pgjdbc/"/></li>
 * </ul>
 */

package io.crate.example.testing;

import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Properties;

public class Application {

    public record Results(ResultSetMetaData metaData, List<Object[]> rows) {}

    private final String dsn;
    private final String user;

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
            throw new IllegalArgumentException(
                    """
                    ERROR: Need a single argument, the database connection URL.
                    
                    Examples:
                    ./gradlew run --args="jdbc:crate://localhost:5432/"
                    ./gradlew run --args="jdbc:postgresql://localhost:5432/"
                    """);
        }
        String connectionUrl = args[0];
        Application app = new Application(connectionUrl);
        printResults(app.querySummitsTable());
        System.out.println("Done.");
    }

    public static void printResults(Results results) throws SQLException {
        for (int i = 0; i < results.rows.size(); i++) {
            Object[] row = results.rows.get(i);
            System.out.printf(Locale.ENGLISH, "> row %d%n", i + 1);
            for (int j = 1; j < results.metaData().getColumnCount(); j++) {
                System.out.printf(
                        Locale.ENGLISH,
                        ">> col %d: %s: %s%n",
                        j,
                        results.metaData.getColumnName(j),
                        row[j]);
            }
            System.out.println();
        }
    }

    /**
     * Example database conversation: Query the built-in `sys.summits` table of CrateDB.
     */
    public Results querySummitsTable() throws IOException, SQLException {
        return this.query("SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3");
    }

    public Results showCreateTable(String tablename) throws IOException, SQLException {
        return this.query("SHOW CREATE TABLE " + tablename);
    }

    public Results query(String sql) throws IOException, SQLException {
        Properties connectionProps = new Properties();
        connectionProps.put("user", user);

        try (Connection sqlConnection = DriverManager.getConnection(dsn, connectionProps)) {
            sqlConnection.setAutoCommit(true);
            if (sqlConnection.isClosed()) {
                throw new IOException("ERROR: Unable to open connection to database");
            }
            try (Statement stmt = sqlConnection.createStatement()) {
                boolean checkResults = stmt.execute(sql);
                if (checkResults) {
                    List<Object[]> rows = new ArrayList<>();
                    ResultSet rs = stmt.getResultSet();
                    while (rs.next()) {
                        ResultSetMetaData metaData = rs.getMetaData();
                        int columnCount = metaData.getColumnCount();
                        Object[] row = new Object[columnCount];
                        for (int i = 1; i < columnCount; i++) {
                            row[i] = rs.getObject(i);
                        }
                        rows.add(row);
                    }
                    return new Results(rs.getMetaData(), rows);
                } else {
                    throw new IOException("ERROR: Result is empty");
                }
            }
        }
    }
}
