package io.crate.example.testing;

import io.crate.example.testing.utils.TestingHelpers;
import org.junit.ClassRule;
import org.junit.Test;
import org.testcontainers.cratedb.CrateDBContainer;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.example.testing.utils.TestingHelpers.assertResults;


/**
 * Class-scoped testcontainer instance with JUnit 4 @Rule/@ClassRule integration.
 * <p>
 * In case you can't use the URL support, or need to fine-tune the container, you can instantiate it yourself.
 * Note that if you use @Rule, you will be given an isolated container for each test method.
 * If you use @ClassRule, you will get on isolated container for all the methods in the test class.
 * </p>
 * <p>
 *   <a href="https://www.testcontainers.org/modules/databases/jdbc/#database-container-objects"/>
 *   <a href="https://www.testcontainers.org/test_framework_integration/junit_4/#ruleclassrule-integration"/>
 * </p>
 */
public class TestClassScope {

    @ClassRule
    public static CrateDBContainer cratedb = new CrateDBContainer(TestingHelpers.nameFromLabel("5.2"));

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
