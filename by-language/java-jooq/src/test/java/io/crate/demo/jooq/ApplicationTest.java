package io.crate.demo.jooq;

import org.jooq.DSLContext;
import org.jooq.impl.DSL;
import org.junit.Assert;
import org.junit.Test;

import java.io.IOException;
import java.sql.SQLException;

import static io.crate.demo.jooq.model.Tables.AUTHOR;

public class ApplicationTest {

    /**
     * Run demo application example with generated code, and verify it works.
     */
    @Test
    public void testExampleWithGeneratedCode() throws SQLException, IOException {

        // Invoke example.
        Application app = new Application();
        app.exampleWithGeneratedCode();

        // Check number of records.
        DSLContext db = app.getDSLContext();
        int count = db.fetchCount(DSL.selectFrom(AUTHOR));
        Assert.assertEquals(count, 3);
    }

    /**
     * Run demo application example with generated code, and verify it works.
     */
    @Test
    public void testExampleWithDynamicSchema() throws SQLException, IOException {

        // Invoke example.
        Application app = new Application();
        app.exampleWithDynamicSchema();

        // Check number of records.
        DSLContext db = app.getDSLContext();
        int count = db.fetchCount(DSL.selectFrom("testdrive.book"));
        Assert.assertEquals(count, 2);
    }

}
