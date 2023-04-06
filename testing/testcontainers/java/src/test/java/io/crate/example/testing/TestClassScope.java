package io.crate.example.testing;

import org.junit.ClassRule;
import org.junit.Test;

import java.io.IOException;
import java.sql.SQLException;

import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;


/**
 * Class-scoped testcontainer instance with JUnit 4 @Rule/@ClassRule integration.
 *
 * In case you can't use the URL support, or need to fine-tune the container, you can instantiate it yourself.
 * Note that if you use @Rule, you will be given an isolated container for each test method.
 * If you use @ClassRule, you will get on isolated container for all the methods in the test class.
 *
 * - https://www.testcontainers.org/modules/databases/jdbc/#database-container-objects
 * - https://www.testcontainers.org/test_framework_integration/junit_4/#ruleclassrule-integration
 */
public class TestClassScope {
    @ClassRule
    public static CrateDBContainer cratedb = new CrateDBContainer(DockerImageName.parse("crate:5.2"));

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
