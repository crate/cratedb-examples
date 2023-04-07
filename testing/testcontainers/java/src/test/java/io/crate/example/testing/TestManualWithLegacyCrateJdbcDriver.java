package io.crate.example.testing;

import org.junit.Test;
import org.testcontainers.containers.JdbcDatabaseContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.utility.DockerImageName;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.example.testing.utils.TestingHelpers.assertResults;


/**
 * Function-scoped testcontainer instance with manual setup/teardown, using a custom CrateDBContainer which uses
 * the <a href="https://crate.io/docs/jdbc/en/latest/index.html">legacy CrateDB JDBC driver</a>.
 * <a href="https://www.testcontainers.org/test_framework_integration/junit_4/#manually-controlling-container-lifecycle" />
 */
public class TestManualWithLegacyCrateJdbcDriver {

    @Test
    public void testReadSummits() throws SQLException, IOException {
        // Run CrateDB nightly.
        DockerImageName image = DockerImageName.parse("crate/crate:nightly").asCompatibleSubstituteFor("crate");
        try (CrateDBContainerLegacyJdbcDriver cratedb = new CrateDBContainerLegacyJdbcDriver(image)) {
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

    static class CrateDBContainerLegacyJdbcDriver extends JdbcDatabaseContainer<CrateDBContainerLegacyJdbcDriver> {

        public static final String IMAGE = "crate";

        protected static final DockerImageName DEFAULT_IMAGE_NAME = DockerImageName.parse(IMAGE);

        private String databaseName = "crate";

        private String username = "crate";

        private String password = "crate";

        public CrateDBContainerLegacyJdbcDriver(final DockerImageName dockerImageName) {
            super(dockerImageName);
            dockerImageName.assertCompatibleWith(DEFAULT_IMAGE_NAME);

            this.waitStrategy = Wait.forHttp("/").forPort(4200).forStatusCode(200);

            addExposedPort(5432);
            addExposedPort(4200);
        }

        @Override
        public String getDriverClassName() {
            return "io.crate.client.jdbc.CrateDriver";
        }

        @Override
        public String getJdbcUrl() {
            String additionalUrlParams = constructUrlParameters("?", "&");
            return ("jdbc:crate://"
                    + getHost()
                    + ":"
                    + getMappedPort(5432)
                    + "/"
                    + databaseName
                    + additionalUrlParams);
        }

        @Override
        public String getDatabaseName() {
            return databaseName;
        }

        @Override
        public String getUsername() {
            return username;
        }

        @Override
        public String getPassword() {
            return password;
        }

        @Override
        public String getTestQueryString() {
            return "SELECT 1";
        }

        @Override
        public CrateDBContainerLegacyJdbcDriver withDatabaseName(final String databaseName) {
            this.databaseName = databaseName;
            return self();
        }

        @Override
        public CrateDBContainerLegacyJdbcDriver withUsername(final String username) {
            this.username = username;
            return self();
        }

        @Override
        public CrateDBContainerLegacyJdbcDriver withPassword(final String password) {
            this.password = password;
            return self();
        }

        @Override
        protected void waitUntilContainerStarted() {
            getWaitStrategy().waitUntilReady(this);
        }
    }
}
