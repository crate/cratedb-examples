package io.crate.example.testing;

import org.junit.Test;

import java.io.IOException;
import java.sql.SQLException;

import static org.assertj.core.api.Assertions.assertThat;


/**
 * Database containers launched with SQL initialization/provisioning script/routine.
 * <p>
 *   <a href="https://www.testcontainers.org/modules/databases/jdbc/#database-containers-launched-via-jdbc-url-scheme"/>
 *   <a href="https://www.testcontainers.org/features/reuse/"/>
 * </p>
 */
public class TestSqlInitialization {

    /**
     * Launch container with CrateDB 5.2, using `TC_INITSCRIPT` to address a file in Java's CLASSPATH.
     * <a href="https://www.testcontainers.org/modules/databases/jdbc/#using-a-classpath-init-script"/>
     */
    @Test
    public void testTcInitClasspathFile() throws SQLException, IOException {
        String connectionUrl = "jdbc:tc:cratedb:5.2://localhost/doc?user=crate&TC_REUSABLE=true&TC_INITSCRIPT=init.sql";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke `SHOW CREATE TABLE ...` query.
        Application app = new Application(connectionUrl);
        var results= app.showCreateTable("alltypes");
        assertThat(results.metaData().getColumnCount()).isEqualTo(1);
        assertThat(results.rows()).hasSize(1);
    }

    /**
     * Launch container with CrateDB 5.2, using `TC_INITSCRIPT` to address an arbitrary file on the filesystem.
     * <a href="https://www.testcontainers.org/modules/databases/jdbc/#using-an-init-script-from-a-file"/>
     */
    @Test
    public void testTcInitArbitraryFile() throws SQLException, IOException {
        String connectionUrl = "jdbc:tc:cratedb:5.2://localhost/doc?user=crate&TC_REUSABLE=true&TC_INITSCRIPT=file:src/test/resources/init.sql";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke `SHOW CREATE TABLE ...` query.
        Application app = new Application(connectionUrl);
        var results= app.showCreateTable("alltypes");
        assertThat(results.metaData().getColumnCount()).isEqualTo(1);
        assertThat(results.rows()).hasSize(1);
    }

    /**
     * Launch container with CrateDB 5.2, using an init function.
     * <a href="https://www.testcontainers.org/modules/databases/jdbc/#using-an-init-script-from-a-file"/>
     */
    @Test
    public void testTcInitFunction() throws SQLException, IOException {
        String connectionUrl = "jdbc:tc:cratedb:5.2://localhost/doc?user=crate&TC_INITFUNCTION=io.crate.example.testing.utils.TestingHelpers::sqlInitFunction";
        System.out.printf("Connecting to %s%n", connectionUrl);

        // Invoke `SHOW CREATE TABLE ...` query.
        Application app = new Application(connectionUrl);
        var results= app.showCreateTable("foobar_init");
        assertThat(results.metaData().getColumnCount()).isEqualTo(1);
        assertThat(results.rows()).hasSize(1);
    }
}
