package io.crate.example.testing;

import io.crate.example.testing.utils.TestingHelpers;
import org.junit.Before;
import org.junit.Test;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.example.testing.utils.TestingHelpers.assertResults;


/**
 * Testcontainer instance shared across multiple test classes, implemented using the Singleton pattern.
 * This test case uses the CrateDB nightly release.
 * <p>
 * Sometimes it might be useful to define a container that is only started
 * once for several test classes. There is no special support for this use
 * case provided by the Testcontainers extension. Instead, this can be
 * implemented using the Singleton pattern.
 * </p>
 * <a href="https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers"/>
 */
public class TestSharedSingleton {

    private CrateDBContainer cratedb;

    @Before
    public void startContainer() {
        // Run CrateDB latest.
        DockerImageName image = TestingHelpers.nameFromLabel("latest");
        cratedb = new CrateDBContainer(image);
        cratedb.start();
    }

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
