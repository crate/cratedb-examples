import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.util.Properties;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;

public class BasicPostgresCrateDB {

    @Parameter(names = {"--dburl", "-d"}, description = "Database URL")
    String dburl;
    @Parameter(names = {"--user", "-u"}, description = "Username")
    String user = "crate";
    @Parameter(names = {"--password", "-p"}, description = "Password")
    String password = "";

    @Parameter(names = "--help", help = true, description = "Display this page")
    private boolean help;

    public static final int SO_RCVBUF = 1024 * 1024; // 1 MB
    public static final int MAX_BATCH_SIZE = 10000;
    public static final int QUERY_EXECUTION_TIMEOUT_SECS = 60;

    public static void main(String ... argv) throws Exception {

        BasicPostgresCrateDB main = new BasicPostgresCrateDB();
        JCommander jc = JCommander.newBuilder()
                .addObject(main)
                .build();
        jc.setProgramName("cratedb-jdbc-example");
        jc.parse(argv);
        int exitcode = main.run(jc);
        System.exit(exitcode);
    }
    public int run(JCommander jc) throws Exception {
        /*
         * Connect to CrateDB and query `sys.summits` table.
         * https://jdbc.postgresql.org/documentation/head/connect.html
         */
        if (help) {
            jc.usage();
            return 0;
        }

        String connectionUrl = dburl;

        Properties connectionProps = new Properties();
        connectionProps.put("user", user);
        connectionProps.put("password", password);
        connectionProps.put("recvBufferSize", SO_RCVBUF);
        connectionProps.put("defaultRowFetchSize", MAX_BATCH_SIZE);
        connectionProps.put("loginTimeout", 5); // seconds, fail fast-ish
        connectionProps.put("socketTimeout", QUERY_EXECUTION_TIMEOUT_SECS);
        connectionProps.put("tcpKeepAlive", true);

        try (Connection sqlConnection = DriverManager.getConnection(connectionUrl, connectionProps)) {
            /*
             * CREATE TABLE "doc"."ti1" ("a" OBJECT(DYNAMIC));
             */
            PreparedStatement st = sqlConnection.prepareStatement("INSERT INTO doc.ti1 VALUES (?)");
            st.setString(1, "{\"a\" 1}");
            st.executeUpdate();
            st.close();

            sqlConnection.close();
        } catch (Exception ex) {
            System.out.println("ERROR: " + ex);
            return 1;
        }
        return 0;
    }
}
