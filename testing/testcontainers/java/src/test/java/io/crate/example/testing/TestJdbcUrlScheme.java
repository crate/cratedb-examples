package io.crate.example.testing;

import org.junit.Test;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.example.testing.Application.printResults;
import static io.crate.example.testing.utils.TestingHelpers.assertResults;


/**
 * Database containers launched via Testcontainers "TC" JDBC URL scheme.
 * <p>
 *   <a href="https://www.testcontainers.org/modules/databases/jdbc/#database-containers-launched-via-jdbc-url-scheme"/>
 *   <a href="https://www.testcontainers.org/features/reuse/"/>
 * </p>
 */
public class TestJdbcUrlScheme {

    /**
     * Launch container with PostgreSQL.
     */
    @Test
    public void testReadSummitsPostgreSQL() throws SQLException, IOException {
        String connectionUrl = "jdbc:tc:postgresql:17:///";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke example query.
        Application app = new Application(connectionUrl, "postgres");
        printResults(app.query("SELECT * FROM information_schema.sql_features LIMIT 3;"));
    }

    /**
     * Launch container with CrateDB.
     */
    @Test
    public void testReadSummitsCrateDB() throws SQLException, IOException {
        // NOTE: Please note `jdbc:tc:crate` will not work, only `jdbc:tc:cratedb`.
        //       => `java.lang.UnsupportedOperationException: Database name crate not supported`
        String connectionUrl = "jdbc:tc:cratedb:5.10://localhost/doc?user=crate";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke example query.
        Application app = new Application(connectionUrl);
        var results = app.querySummitsTable();
        assertResults(results);
    }

    /**
     * Launch container with CrateDB, using daemon mode.
     * <a href="https://www.testcontainers.org/modules/databases/jdbc/#running-container-in-daemon-mode"/>
     */
    @Test
    public void testReadSummitsCrateDBWithDaemon() throws SQLException, IOException {
        String connectionUrl = "jdbc:tc:cratedb:5.10://localhost/doc?user=crate&TC_DAEMON=true";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke example query.
        Application app = new Application(connectionUrl);
        var results = app.querySummitsTable();
        assertResults(results);
    }

    /**
     * Launch container with CrateDB, using "Reusable Containers (Experimental)".
     * <a href="https://www.testcontainers.org/features/reuse/"/>
     */
    @Test
    public void testReadSummitsCrateDBWithReuse() throws SQLException, IOException {
        String connectionUrl = "jdbc:tc:cratedb:5.10://localhost/doc?user=crate&TC_REUSABLE=true";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke example query.
        Application app = new Application(connectionUrl);
        var results = app.querySummitsTable();
        assertResults(results);
    }
}
