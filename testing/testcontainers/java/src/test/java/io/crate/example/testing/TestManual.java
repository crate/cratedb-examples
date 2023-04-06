package io.crate.example.testing;

import org.junit.Test;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;

import java.io.IOException;
import java.sql.SQLException;


/**
 * Function-scoped testcontainer instance with manual setup/teardown.
 *
 * - https://www.testcontainers.org/test_framework_integration/junit_4/#manually-controlling-container-lifecycle
 */
public class TestManual {

    @Test
    public void testReadSummits() throws SQLException, IOException {

        // Run CrateDB nightly.
        DockerImageName image = DockerImageName.parse("crate/crate:nightly").asCompatibleSubstituteFor("crate");
        CrateDBContainer cratedb = new CrateDBContainer(image);
        cratedb.start();

        // Get JDBC URL to CrateDB instance.
        String connectionUrl = cratedb.getJdbcUrl();
        System.out.println(String.format("Connecting to %s", connectionUrl));

        // Invoke example test.
        Application app = new Application(connectionUrl);
        app.querySummitsTable();

        // Tear down CrateDB.
        cratedb.stop();

    }

}
