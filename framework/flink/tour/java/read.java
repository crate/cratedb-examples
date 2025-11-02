// Read from CrateDB using Apache Flink.
// Invoke: gradle run read
// Source: https://github.com/crate/cratedb-examples/blob/main/framework/flink/tour/java/read.java

// https://tacnode.io/docs/guides/ecosystem/bigdata/flink#catalog-registration
// https://github.com/crate/cratedb-flink-jobs/blob/main/src/main/java/io/crate/flink/demo/SimpleTableApiJob.java
// https://nightlies.apache.org/flink/flink-docs-release-1.20/docs/connectors/table/jdbc/#jdbc-catalog-for-postgresql
import org.apache.flink.connector.jdbc.catalog.JdbcCatalog;
import org.apache.flink.table.api.*;

import static org.apache.flink.table.api.Expressions.$;

public class read {

    public static String CATALOG_NAME = "example_catalog";

    public static void main(String[] args) throws Exception {

        // Create Flink Table API environment.
        EnvironmentSettings settings = EnvironmentSettings.inStreamingMode();
        TableEnvironment env = TableEnvironment.create(settings);

        // Define catalog.
        // CrateDB only knows a single database called `crate`,
        // but you can separate concerns using schemata. The
        // default schema is `doc`.
        JdbcCatalog catalog = new JdbcCatalog(
            CATALOG_NAME,
            "crate",
            "crate",
            "crate",
            "jdbc:crate://localhost:5432"
            );

        // Register catalog and set as default.
        env.registerCatalog(CATALOG_NAME, catalog);
        env.useCatalog(CATALOG_NAME);

        // Invoke query using plain SQL.
        // FIXME: Currently does not work with `sys.summits`.
        // SqlValidatorException: Object 'sys.summits' not found
        env.executeSql("SELECT * FROM `doc.person` LIMIT 3").print();

        // Invoke query using DSL.
        env.from("`doc.person`")
                .select($("name"), $("age"))
                .execute()
                .print();
    }

}
