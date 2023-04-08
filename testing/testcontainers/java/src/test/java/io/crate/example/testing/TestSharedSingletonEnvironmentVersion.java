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
 * Testcontainer instance honoring the `CRATEDB_VERSION` environment variable,
 * suitable for running a test matrix on different versions of CrateDB.
 * <p>
 * Possible values are:
 * <ul>
 *     <li>Version numbers: 5, 5.2, 5.2.3, etc.</li>
 *     <li>Latest release: latest</li>
 *     <li>Nightly release: nightly</li>
 * </ul>
 * </p>
 */
public class TestSharedSingletonEnvironmentVersion {

    private CrateDBContainer cratedb;

    @Before
    public void startContainer() {
        // Run designated CrateDB version.
        DockerImageName image = TestingHelpers.nameFromEnvironment();
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
