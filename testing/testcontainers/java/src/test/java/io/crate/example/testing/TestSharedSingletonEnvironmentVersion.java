package io.crate.example.testing;

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
abstract class AbstractContainerSingletonEnvironmentVersion {

    static final CrateDBContainer cratedb;

    static {

        String cratedb_version = System.getenv("CRATEDB_VERSION");
        String fullImageName;
        if (cratedb_version == null) {
            fullImageName = "crate:latest";
        } else {
            if (cratedb_version.equals("nightly")) {
                fullImageName = "crate/crate:nightly";
            } else {
                fullImageName = String.format("crate:%s", cratedb_version);
            }
        }

        // Run designated CrateDB version.
        DockerImageName image = DockerImageName.parse(fullImageName).asCompatibleSubstituteFor("crate");
        cratedb = new CrateDBContainer(image);
        cratedb.start();
    }
}


public class TestSharedSingletonEnvironmentVersion extends AbstractContainerSingletonEnvironmentVersion {

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
