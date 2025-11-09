package io.crate.example.testing;

import io.crate.example.testing.utils.TestingHelpers;
import org.junit.jupiter.api.Test;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.example.testing.utils.TestingHelpers.assertResults;


/**
 * Function-scoped testcontainer instance with JUnit 5.
 * <p>
 * The extension finds all fields that are annotated with @Container and calls their container
 * lifecycle methods (methods on the Startable interface).
 * Containers declared as instance fields will be started and stopped for every test method.
 * </p>
 * <p>
 *   <a href="https://java.testcontainers.org/test_framework_integration/junit_5/#restarted-containers"/>
 * </p>
 */
@Testcontainers
public class TestFunctionScope {

    @Container
    public CrateDBContainer cratedb = new CrateDBContainer(TestingHelpers.nameFromLabel("5.10"));

    @Test
    public void testReadSummits() throws SQLException, IOException {

        // Get JDBC URL to CrateDB instance.
        String connectionUrl = cratedb.getJdbcUrl();
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke example test.
        Application app = new Application(connectionUrl);
        var results = app.querySummitsTable();
        assertResults(results);
    }
}
