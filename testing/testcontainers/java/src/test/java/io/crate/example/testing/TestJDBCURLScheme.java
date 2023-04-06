package io.crate.example.testing;

import org.junit.Test;

import java.io.IOException;
import java.sql.SQLException;


/**
 * Database containers launched via Testcontainers "TC" JDBC URL scheme.
 *
 * - https://www.testcontainers.org/modules/databases/jdbc/#database-containers-launched-via-jdbc-url-scheme
 * - https://www.testcontainers.org/features/reuse/
 */
public class TestJDBCURLScheme {

    /**
     * Launch container with PostgreSQL 15.
     */
    @Test
    public void testReadSummitsPostgreSQL() throws SQLException, IOException {

        String connectionUrl = "jdbc:tc:postgresql:15:///";
        System.out.println(String.format("Connecting to %s", connectionUrl));

        // Invoke example query.
        Application app = new Application(connectionUrl, "postgres");
        app.query("SELECT * FROM information_schema.sql_features LIMIT 3;");
    }

    /**
     * Launch container with CrateDB 5.2.
     */
    @Test
    public void testReadSummitsCrateDB() throws SQLException, IOException {

        // NOTE: Please note `jdbc:tc:crate` will not work, only `jdbc:tc:cratedb`.
        //       => `java.lang.UnsupportedOperationException: Database name crate not supported`
        String connectionUrl = "jdbc:tc:cratedb:5.2://localhost/doc?user=crate";
        System.out.println(String.format("Connecting to %s", connectionUrl));

        // Invoke example query.
        Application app = new Application(connectionUrl);
        app.querySummitsTable();

    }

    /**
     * Launch container with CrateDB 5.2, using daemon mode.
     *
     * https://www.testcontainers.org/modules/databases/jdbc/#running-container-in-daemon-mode
     */
    @Test
    public void testReadSummitsCrateDBWithDaemon() throws SQLException, IOException {

        String connectionUrl = "jdbc:tc:cratedb:5.2://localhost/doc?user=crate&TC_DAEMON=true";
        System.out.println(String.format("Connecting to %s", connectionUrl));

        // Invoke example query.
        Application app = new Application(connectionUrl);
        app.querySummitsTable();

    }

    /**
     * Launch container with CrateDB 5.2, using "Reusable Containers (Experimental)".
     *
     * https://www.testcontainers.org/features/reuse/
     */
    @Test
    public void testReadSummitsCrateDBWithReuse() throws SQLException, IOException {

        String connectionUrl = "jdbc:tc:cratedb:5.2://localhost/doc?user=crate&TC_REUSABLE=true";
        System.out.println(String.format("Connecting to %s", connectionUrl));

        // Invoke example query.
        Application app = new Application(connectionUrl);
        app.querySummitsTable();

    }

}
