package io.crate.example.testing;

import org.junit.Test;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;

import java.io.IOException;
import java.sql.SQLException;


/**
 * Testcontainer instance honoring the `CRATEDB_VERSION` environment variable,
 * suitable for running a test matrix on different versions of CrateDB.
 *
 * Possible values are:
 * - Version numbers: 5, 5.2, 5.2.3
 * - Nightly release: nightly
 */
abstract class AbstractContainerMatrixBaseTest {

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


public class TestSharedSingletonMatrix extends AbstractContainerMatrixBaseTest {

    @Test
    public void testReadSummits() throws SQLException, IOException {

        // Get JDBC URL to CrateDB instance.
        String connectionUrl = cratedb.getJdbcUrl();
        System.out.println(String.format("Connecting to %s", connectionUrl));

        // Invoke example test.
        Application app = new Application(connectionUrl);
        app.querySummitsTable();

    }

}
