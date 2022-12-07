import java.sql.ResultSet;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.DriverManager;
import java.sql.ResultSetMetaData;
import java.util.Locale;
import java.util.Properties;

public class BasicPostgresCrateDB {

    public static final int SO_RCVBUF = 1024 * 1024; // 1 MB
    public static final int MAX_BATCH_SIZE = 20000;
    public static final int QUERY_EXECUTION_TIMEOUT_SECS = 60;


    public static void main(String[] args) throws Exception {

        // Create schema and insert data:
        //
        // psql postgres://crate@localhost:5432/
        //
        // CREATE TABLE testdrive (id INT PRIMARY KEY, data TEXT);
        // INSERT INTO testdrive VALUES (0, 'zero'), (1, 'one'), (2, 'two');

        // String connectionUrl = "jdbc:postgresql://localhost:5432/";
        // String connectionUrl = "jdbc:crate://localhost:5432/";
        String connectionUrl = args[0];

        Properties connectionProps = new Properties();
        // https://jdbc.postgresql.org/documentation/head/connect.html
        connectionProps.put("user", "crate");
        connectionProps.put("password", "");
        connectionProps.put("ssl", false);
        connectionProps.put("recvBufferSize", SO_RCVBUF);
        connectionProps.put("defaultRowFetchSize", MAX_BATCH_SIZE);
        connectionProps.put("loginTimeout", 5); // seconds, fail fast-ish
        connectionProps.put("socketTimeout", QUERY_EXECUTION_TIMEOUT_SECS);
        connectionProps.put("tcpKeepAlive", true);


        try (Connection sqlConnection = DriverManager.getConnection(connectionUrl, connectionProps)) {
            sqlConnection.setAutoCommit(true);
            if (sqlConnection.isClosed()) {
                System.out.println("Connection is not valid");
                return;
            }
            try(Statement stmt = sqlConnection.createStatement()) {
                boolean checkResults = stmt.execute("select * from testdrive");
                if (checkResults) {
                    ResultSet rs = stmt.getResultSet();
                    while (rs.next()) {
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
                }
            }
        }
    }
}
