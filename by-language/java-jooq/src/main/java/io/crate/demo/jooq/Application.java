package io.crate.demo.jooq;

import org.jooq.Record;
import org.jooq.*;
import org.jooq.conf.Settings;
import org.jooq.impl.DSL;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

import io.crate.demo.jooq.model.tables.records.AuthorRecord;
import static io.crate.demo.jooq.model.Tables.AUTHOR;
import static org.jooq.impl.DSL.field;
import static org.jooq.impl.DSL.table;


/**
 * A demo application using CrateDB with jOOQ and the PostgreSQL JDBC driver.
 *
 * - https://github.com/crate/crate
 * - https://github.com/jOOQ/jOOQ
 * - https://github.com/pgjdbc/pgjdbc
 */
public class Application {

    public static void main(String[] args) throws IOException, SQLException {
        Application app = new Application();

        Tools.title("Example with generated code");
        app.exampleWithGeneratedCode();

        Tools.title("Example with dynamic schema");
        app.exampleWithDynamicSchema();

        System.out.println("Ready.");
    }

    /**
     * Create a new jOOQ DefaultDSLContext instance, wrapping the database connection.
     *
     * It will use database connection settings from the `application.properties` file,
     * and will also enable SQL command logging for demonstration purposes.
     */
    public DSLContext getDSLContext() throws SQLException {

        // Disable the jOOQ self-ad/banner and its tip of the day.
        System.setProperty("org.jooq.no-logo", "true");
        System.setProperty("org.jooq.no-tips", "true");

        // Read settings from `application.properties` file.
        Properties app_settings = Tools.readSettingsFile("application.properties");

        // Read database settings.
        String DS_URL = app_settings.getProperty("application.datasource.url");
        String DS_USERNAME = app_settings.getProperty("application.datasource.username");
        String DS_PASSWORD = app_settings.getProperty("application.datasource.password");

        // Connect to the database, with given settings and parameters, and select the PostgreSQL dialect.
        Settings db_settings = new Settings();
        db_settings.setExecuteLogging(true);
        Connection connection = DriverManager.getConnection(DS_URL, DS_USERNAME, DS_PASSWORD);
        return DSL.using(connection, SQLDialect.POSTGRES, db_settings);
    }

    /**
     * jOOQ as a SQL builder with code generation [1]
     *
     * > Use jOOQ's code generation features in order to compile your SQL
     * > statements using a Java compiler against an actual database schema.
     * >
     * > This adds a lot of power and expressiveness to just simply
     * > constructing SQL using the query DSL and custom strings and
     * > literals, as you can be sure that all database artefacts actually
     * > exist in the database, and that their type is correct.
     * > We strongly recommend using this approach.
     *
     * [1] https://www.jooq.org/doc/latest/manual/getting-started/use-cases/jooq-as-a-sql-builder-with-code-generation/
     *
     * TODO: Code generation is currently not possible with CrateDB, because,
     *       with the PostgreSQL dialect, jOOQ issues a CTE using the
     *       `WITH RECURSIVE` directive to reflect the database schema.
     *       For this example, the "generated" code has been written manually.
     *
     */
    public void exampleWithGeneratedCode() throws IOException, SQLException {

        DSLContext db = getDSLContext();

        // Create table.
        String bootstrap_sql = Tools.readTextFile("bootstrap.sql");
        db.query(bootstrap_sql).execute();

        // Truncate table.
        db.delete(AUTHOR).where(DSL.trueCondition()).execute();
        db.query(String.format("REFRESH TABLE %s", AUTHOR)).execute();

        // Insert records.
        InsertSetMoreStep<AuthorRecord> new_record1 = db.insertInto(AUTHOR).set(AUTHOR.ID, 1).set(AUTHOR.NAME, "John Doe");
        InsertSetMoreStep<AuthorRecord> new_record2 = db.insertInto(AUTHOR).set(AUTHOR.ID, 2).set(AUTHOR.NAME, "Jane Doe");
        InsertSetMoreStep<AuthorRecord> new_record3 = db.insertInto(AUTHOR).set(AUTHOR.ID, 3).set(AUTHOR.NAME, "Jack Black");
        new_record1.execute();
        new_record2.execute();
        new_record3.execute();
        db.query(String.format("REFRESH TABLE %s", AUTHOR)).execute();

        // Fetch records, with filtering and sorting.
        Result<Record> result = db.select()
                .from(AUTHOR)
                .where(AUTHOR.NAME.like("Ja%"))
                .orderBy(AUTHOR.NAME)
                .fetch();

        // Display result.
        // System.out.println("Result:");
        // System.out.println(result);

        // Iterate and display records.
        System.out.println("By record:");
        for (Record record : result) {
            Integer id = record.getValue(AUTHOR.ID);
            String name = record.getValue(AUTHOR.NAME);
            System.out.println("id: " + id + ", name: " + name);
        }
        System.out.println();

    }

    /**
     * jOOQ as a standalone SQL builder without code generation [1]
     *
     * If you have a dynamic schema, you don't have to use the code generator.
     * This is the simplest of all use cases, allowing for construction of
     * valid SQL for any database. In this use case, you will not use jOOQ's
     * code generator and maybe not even jOOQ's query execution facilities.
     *
     * Instead, you'll use jOOQ's query DSL API to wrap strings, literals and
     * other user-defined objects into an object-oriented, type-safe AST
     * modelling your SQL statements.
     *
     * [1] https://www.jooq.org/doc/latest/manual/getting-started/use-cases/jooq-as-a-sql-builder-without-codegeneration/
     *
     */
    public void exampleWithDynamicSchema() throws IOException, SQLException {

        DSLContext db = getDSLContext();

        Table<Record> BOOK = table("book");
        Field<Object> BOOK_ID = field("id");
        Field<Object> BOOK_TITLE = field("title");

        // Create table.
        String bootstrap_sql = Tools.readTextFile("bootstrap.sql");
        db.query(bootstrap_sql).execute();

        // Truncate table.
        db.delete(BOOK).where(DSL.trueCondition()).execute();
        db.query(String.format("REFRESH TABLE %s", BOOK)).execute();

        // Insert records.
        InsertSetMoreStep<Record> new_record1 = db.insertInto(BOOK).set(BOOK_ID, 1).set(BOOK_TITLE, "Foo");
        InsertSetMoreStep<Record> new_record2 = db.insertInto(BOOK).set(BOOK_ID, 2).set(BOOK_TITLE, "Bar");
        new_record1.execute();
        new_record2.execute();
        db.query(String.format("REFRESH TABLE %s", BOOK)).execute();

        // Fetch records, with filtering and sorting.
        Result<Record> result = db.select()
                .from(BOOK)
                .where(BOOK_TITLE.like("B%"))
                .orderBy(BOOK_TITLE)
                .fetch();

        // Display result.
        // System.out.println("Result:");
        // System.out.println(result);

        // Iterate and display records.
        System.out.println("By record:");
        for (Record record : result) {
            // TODO: How can we know about the index positions of the corresponding columns?
            Integer id = (Integer) record.getValue(0);
            String title = (String) record.getValue(1);
            System.out.println("id: " + id + ", title: " + title);
        }
        System.out.println();

    }

}
