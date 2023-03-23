import java.sql.ResultSet;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.DriverManager;
import java.sql.ResultSetMetaData;
import java.util.Locale;
import java.util.Properties;
import com.beust.jcommander.Parameter;
import com.beust.jcommander.JCommander;

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
        //connectionProps.put("ssl", "true");
        connectionProps.put("recvBufferSize", SO_RCVBUF);
        connectionProps.put("defaultRowFetchSize", MAX_BATCH_SIZE);
        connectionProps.put("loginTimeout", 5); // seconds, fail fast-ish
        connectionProps.put("socketTimeout", QUERY_EXECUTION_TIMEOUT_SECS);
        connectionProps.put("tcpKeepAlive", true);

        try (Connection sqlConnection = DriverManager.getConnection(connectionUrl, connectionProps)) {
            sqlConnection.setAutoCommit(true);
            if (sqlConnection.isClosed()) {
                System.out.println("ERROR: Unable to open connection to database");
                return 1;
            }
            try (Statement stmt = sqlConnection.createStatement()) {
                boolean checkResults = stmt.execute("SELECT * FROM sys.summits LIMIT 3;");
                if (checkResults) {
                    ResultSet rs = stmt.getResultSet();
                    while (rs.next()) {
                        System.out.printf(Locale.ENGLISH, "> row %d\n", rs.getRow());
                        ResultSetMetaData metaData = rs.getMetaData();
                        int columnCount = metaData.getColumnCount();
                        for (int i = 1; i <= columnCount; i++) {
                            System.out.printf(
                                    Locale.ENGLISH,
                                    ">> col %d: %s: %s\n",
                                    i,
                                    metaData.getColumnName(i),
                                    rs.getObject(i));
                        }
                    }
                } else {
                    System.out.println("WARNING: Result is empty");
                    return 1;
                }
            }
            sqlConnection.close();
        } catch (Exception ex) {
            System.out.println("ERROR: " + ex);
            return 1;
        }
        return 0;
    }
}
