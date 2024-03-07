package io.crate.test;

import io.crate.MyEntity;
import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.sql.DataSource;
import java.security.SecureRandom;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

@QuarkusTest
@QuarkusTestResource(value = CrateDBTestResource.class, restrictToAnnotatedClass = true)
public class CrateDbTest {
    private static final Logger log = LoggerFactory.getLogger(CrateDbTest.class);

    @Inject
    DataSource dataSource;

    private final SecureRandom secureRandom = new SecureRandom();

    @Test
    public void testCorrectNumberInserted() {
        int randomNumber = secureRandom.nextInt(100) + 1;

        MyEntity.populateWithData(randomNumber);

        refreshTable(MyEntity.class.getSimpleName());

        Assertions.assertEquals(randomNumber, MyEntity.count());

    }

    /**
     * Refresh a table in crate so that it has the correct counts.
     * @param table - the table to refesh
     */
    private void refreshTable(String table) {
        try (Connection connection = dataSource.getConnection();
                Statement statement = connection.createStatement()) {
            // Create a table (if necessary)
            statement.execute("REFRESH TABLE " + table);

        } catch (SQLException e) {
            log.error("Error executing SQL statements", e);
        }
    }

}
