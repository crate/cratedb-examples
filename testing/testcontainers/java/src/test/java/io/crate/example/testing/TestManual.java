package io.crate.example.testing;

import io.crate.example.testing.utils.TestingHelpers;
import org.junit.Test;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.example.testing.utils.TestingHelpers.assertResults;


/**
 * Function-scoped testcontainer instance with manual setup/teardown.
 * <a href="https://www.testcontainers.org/test_framework_integration/junit_4/#manually-controlling-container-lifecycle" />
 */
public class TestManual {

    @Test
    public void testReadSummits() throws SQLException, IOException {
        // Run CrateDB nightly.
        DockerImageName image = TestingHelpers.nameFromLabel("nightly");
        try (CrateDBContainer cratedb = new CrateDBContainer(image)) {
            cratedb.start();

            // Get JDBC URL to CrateDB instance.
            String connectionUrl = cratedb.getJdbcUrl();
            System.out.printf("Connecting to %s%n", connectionUrl);

            // Invoke example test.
            Application app = new Application(connectionUrl);
            var results = app.querySummitsTable();
            assertResults(results);

            // Tear down CrateDB.
            cratedb.stop();
        }
    }
}
