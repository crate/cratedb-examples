package io.crate.example.testing;

import org.junit.Test;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;

import java.io.IOException;
import java.sql.SQLException;


/**
 * Testcontainer instance shared across multiple test classes, implemented using the Singleton pattern.
 *
 * Sometimes it might be useful to define a container that is only started
 * once for several test classes. There is no special support for this use
 * case provided by the Testcontainers extension. Instead, this can be
 * implemented using the Singleton pattern.
 *
 * https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers
 */
abstract class AbstractContainerBaseTest {

    static final CrateDBContainer cratedb;

    static {
        // Run CrateDB nightly.
        DockerImageName image = DockerImageName.parse("crate/crate:nightly").asCompatibleSubstituteFor("crate");
        cratedb = new CrateDBContainer(image);
        cratedb.start();
    }
}


public class TestSharedSingleton extends AbstractContainerBaseTest {

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
