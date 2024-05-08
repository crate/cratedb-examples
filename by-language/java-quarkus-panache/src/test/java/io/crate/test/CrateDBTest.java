package io.crate.test;

import java.security.SecureRandom;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

import javax.sql.DataSource;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.crate.MyEntity;
import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;

@QuarkusTest
@QuarkusTestResource(value = CrateDBTestResource.class, restrictToAnnotatedClass = true)
class CrateDBTest {
    private static final Logger log = LoggerFactory.getLogger(CrateDBTest.class);

    @Inject
    DataSource dataSource;

    private final SecureRandom secureRandom = new SecureRandom();

    @Test
    void testCorrectNumberInserted() {
        int randomNumber = secureRandom.nextInt(100) + 1;

        MyEntity.populateWithData(randomNumber);

        refreshTable(MyEntity.class.getSimpleName());

        Assertions.assertTrue(MyEntity.count() >= randomNumber);

    }

    /**
     * Refresh a table in crate so that it has the correct counts.
     * 
     * @param table - the table to refesh
     */
    private void refreshTable(String table) {
        try (Connection connection = dataSource.getConnection();
                Statement statement = connection.createStatement()) {
            statement.execute("REFRESH TABLE " + table);
        } catch (SQLException e) {
            log.error("Error executing SQL statements", e);
        }
    }

}
