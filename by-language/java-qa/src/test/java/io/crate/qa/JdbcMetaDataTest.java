package stock_jdbc;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.RowIdLifetime;
import java.util.Map;

import org.hamcrest.Matchers;
import org.junit.Assert;
import org.junit.ClassRule;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import io.crate.testing.CrateTestCluster;

@RunWith(JUnit4.class)
public class JdbcMetaDataTest {

    @ClassRule
    public static final CrateTestCluster TEST_CLUSTER = CrateTestCluster
        .fromURL("https://cdn.crate.io/downloads/releases/nightly/crate-latest.tar.gz")
        .settings(Map.of("psql.port", 55432))
        .build();
    public static final String URL = "jdbc:postgresql://localhost:55432/doc?user=crate";

    @Test
    public void test_allProceduresAreCallable() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().allProceduresAreCallable(), is(true));
        }
    }

    @Test
    public void test_allTablesAreSelectable() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().allTablesAreSelectable(), is(true));
        }
    }

    @Test
    public void test_autoCommitFailureClosesAllResultSets() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().autoCommitFailureClosesAllResultSets(), is(false));
        }
    }

    @Test
    public void test_dataDefinitionCausesTransactionCommit_TODO() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().dataDefinitionCausesTransactionCommit(), is(false));
        }
    }

    @Test
    public void test_dataDefinitionIgnoredInTransactions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().dataDefinitionIgnoredInTransactions(), is(false));
        }
    }

    @Test
    public void test_deletesAreDetected() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().deletesAreDetected(ResultSet.TYPE_FORWARD_ONLY), is(false));
        }
    }

    @Test
    public void test_doesMaxRowSizeIncludeBlobs() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().doesMaxRowSizeIncludeBlobs(), is(false));
        }
    }

    @Test
    public void test_generatedKeyAlwaysReturned() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().generatedKeyAlwaysReturned(), is(true));
        }
    }

    @Test
    @Ignore("Not implemented in PostgreSQL JDBC")
    public void test_getAttributes() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            conn.getMetaData().getAttributes("", "", "", "");
        }
    }

    @Test
    public void test_getBestRowIdentifier() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var result = conn.getMetaData().getBestRowIdentifier(null, "sys", "summits", DatabaseMetaData.bestRowSession, true);
            assertThat(result.next(), is(true));
        }
    }

    @Test
    public void test_getCatalogSeparator() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getCatalogSeparator(), is("."));
        }
    }

    @Test
    public void test_getCatalogTerm() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getCatalogTerm(), is("database"));
        }
    }

    @Test
    public void test_getCatalogs() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var result = conn.getMetaData().getCatalogs();
            assertThat(result.next(), is(true));
            assertThat(result.getString(1), is("doc"));
        }
    }

    @Test
    public void test_getClientInfoProperties() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var result = conn.getMetaData().getClientInfoProperties();
            assertThat(result.next(), is(true));
            assertThat(result.getString(1), is("ApplicationName"));
        }
    }

    @Test
    @Ignore("https://github.com/crate/crate/issues/9568")
    public void test_getColumnPrivileges() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getColumnPrivileges("", "sys", "summits", "");
            assertThat(results.next(), is(true));
        }
    }

    @Test
    public void test_getColumns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getColumns("", "sys", "summits", "");
            assertThat(results.next(), is(true));
            assertThat(results.getString(3), is("summits"));
            assertThat(results.getString(4), is("classification"));
        }
    }

    @Test
    public void test_getCrossReference() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getCrossReference("", "sys", "jobs", "", "sys", "jobs_log");
            assertThat(results.next(), is(false));
        }
    }

    @Test
    public void test_getDatabaseMajorVersion() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getDatabaseMajorVersion(), is(14));
        }
    }

    @Test
    public void test_getDatabaseMinorVersion() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getDatabaseMinorVersion(), is(0));
        }
    }

    @Test
    public void test_getDatabaseProductName() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getDatabaseProductName(), is("PostgreSQL"));
        }
    }

    @Test
    public void test_getDatabaseProductVersion() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getDatabaseProductVersion(), is("14.0"));
        }
    }

    @Test
    public void test_getDefaultTransactionIsolation() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getDefaultTransactionIsolation(), is(Connection.TRANSACTION_READ_COMMITTED));
        }
    }

    @Test
    public void test_getExportedKeys() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getExportedKeys("", "sys", "summits");
            assertThat(results.next(), is(false));
        }
    }

    @Test
    public void test_getExtraNameCharacters() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getExtraNameCharacters(), is(""));
        }
    }

    @Test
    public void test_getFunctionColumns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getFunctionColumns("", "", "substr", "");
            assertThat(results.next(), is(false));
        }
    }

    @Test
    public void test_getFunctions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getFunctions("", "", "current_schema");
            assertThat(results.next(), is(true));
        }
    }

    @Test
    public void test_getIdentifierQuoteString() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getIdentifierQuoteString(), is("\""));
        }
    }

    @Test
    public void test_getImportedKeys() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getImportedKeys("", "sys", "summits");
            assertThat(results.next(), is(false));
        }
    }

    @Test
    @Ignore("Blocked by https://github.com/crate/crate/issues/5463")
    public void test_getIndexInfo() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getIndexInfo("", "sys", "summits", true, true);
            assertThat(results.next(), is(false));
        }
    }

    @Test
    public void test_getMaxBinaryLiteralLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxBinaryLiteralLength(), is(0));
        }
    }

    @Test
    public void test_getMaxCatalogNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxCatalogNameLength(), is(63));
        }
    }

    @Test
    public void test_getMaxCharLiteralLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxCharLiteralLength(), is(0));
        }
    }

    @Test
    public void test_getMaxColumnNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxColumnNameLength(), is(63));
        }
    }

    @Test
    public void test_getMaxColumnsInGroupBy() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxColumnsInGroupBy(), is(0));
        }
    }

    @Test
    public void test_getMaxColumnsInIndex() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxColumnsInIndex(), is(32));
        }
    }

    @Test
    public void test_getMaxColumnsInOrderBy() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxColumnsInOrderBy(), is(0));
        }
    }

    @Test
    public void test_getMaxColumnsInSelect() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxColumnsInSelect(), is(0));
        }
    }

    @Test
    public void test_getMaxColumnsInTable() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxColumnsInTable(), is(1600));
        }
    }

    @Test
    public void test_getMaxConnections() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxConnections(), is(8192));
        }
    }

    @Test
    public void test_getMaxCursorNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxCursorNameLength(), is(63));
        }
    }

    @Test
    public void test_getMaxIndexLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxIndexLength(), is(0));
        }
    }

    @Test
    public void test_getMaxLogicalLobSize() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxLogicalLobSize(), is(0L));
        }
    }

    @Test
    public void test_getMaxProcedureNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxProcedureNameLength(), is(63));
        }
    }

    @Test
    public void test_getMaxRowSize() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxRowSize(), is(1073741824));
        }
    }

    @Test
    public void test_getMaxSchemaNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxSchemaNameLength(), is(63));
        }
    }

    @Test
    public void test_getMaxStatementLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxStatementLength(), is(0));
        }
    }

    @Test
    public void test_getMaxStatements() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxStatements(), is(0));
        }
    }

    @Test
    public void test_getMaxTableNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxTableNameLength(), is(63));
        }
    }

    @Test
    public void test_getMaxTablesInSelect() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxTablesInSelect(), is(0));
        }
    }

    @Test
    public void test_getMaxUserNameLength() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getMaxUserNameLength(), is(63));
        }
    }

    @Test
    public void tes_getNumericFunctions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(
                conn.getMetaData().getNumericFunctions(),
                is("abs,acos,asin,atan,atan2,ceiling,cos,cot,degrees,exp,floor,log,log10,mod,pi,power,radians,round,sign,sin,sqrt,tan,truncate")
            );
        }
    }

    @Test
    public void test_getPrimaryKeys() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            ResultSet results = conn.getMetaData().getPrimaryKeys(null, null, null);
            assertThat(results.next(), is(true));
        }
    }

    @Test
    public void test_getProcedureColumns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            conn.getMetaData().getProcedureColumns("", "", "", "");
        }
    }

    @Test
    public void test_getProcedureTerm() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getProcedureTerm(), is("function"));
        }
    }

    @Test
    public void test_getProcedures() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            conn.getMetaData().getProcedures("", "", "");
        }
    }

    @Test
    @Ignore("Not implemented by PostgreSQL JDBC")
    public void test_getPseudoColumns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getPseudoColumns("", "sys", "summits", "m");
        }
    }

    @Test
    public void test_getResultSetHoldability() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getResultSetHoldability(), is(ResultSet.HOLD_CURSORS_OVER_COMMIT));
        }
    }

    @Test
    @Ignore("Not implemented by PostgreSQL JDBC")
    public void test_getRowIdLifetime() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getRowIdLifetime(), is(RowIdLifetime.ROWID_UNSUPPORTED));
        }
    }

    @Test
    public void test_getSQLKeywords() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getSQLKeywords(), Matchers.containsString("summary"));
        }
    }

    @Test
    public void test_getSQLStateType() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getSQLStateType(), is(DatabaseMetaData.sqlStateSQL));
        }
    }

    @Test
    public void test_getSchemaTerm() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getSchemaTerm(), is("schema"));
        }
    }

    @Test
    public void test_getSchemas() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getSchemas();
            assertThat(results.next(), is(true));
            assertThat(results.getString(1), is("blob"));
        }
    }

    @Test
    public void test_getSearchStringEscape() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getSearchStringEscape(), is("\\"));
        }
    }

    @Test
    public void test_getStringFunctions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(
                conn.getMetaData().getStringFunctions(),
                is("ascii,char,concat,lcase,left,length,ltrim,repeat,rtrim,space,substring,ucase,replace")
            );
        }
    }

    @Test
    @Ignore("Not implemented in PostgreSQL JDBC")
    public void test_getSuperTables() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            conn.getMetaData().getSuperTables("", "sys", "summits");
        }
    }

    @Test
    @Ignore("Not implemented in PostgreSQL JDBC")
    public void test_getSuperTypes() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            conn.getMetaData().getSuperTypes("", "sys", "t");
        }
    }

    @Test
    public void test_getSystemFunctions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().getSystemFunctions(), is("database,ifnull,user"));
        }
    }

    @Test
    public void test_getTablePrivileges() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getTablePrivileges("", "sys", "summits");
        }
    }

    @Test
    public void test_getTableTypes() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getTableTypes();
            assertThat(results.next(), is(true));
        }
    }

    @Test
    public void test_getTables() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getTables(null, "sys", "", null);
            assertThat(results.next(), is(true));
            assertThat(results.getString(3), is("allocations_pkey"));
        }
    }

    @Test
    public void test_getTimeDateFunctions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(
                conn.getMetaData().getTimeDateFunctions(),
                is("curdate,curtime,dayname,dayofmonth,dayofweek,dayofyear,hour,minute,month,monthname,now,quarter,second,week,year,timestampadd")
            );
        }
    }

    @Test
    public void test_getTypeInfo() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getTypeInfo();
        }
    }

    @Test
    public void test_getUDTs() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            var results = conn.getMetaData().getUDTs("", "sys", "t", new int[0]);
        }
    }

    @Test
    public void test_getVersionColumns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
             var results = conn.getMetaData().getVersionColumns("", "sys", "summits");
             assertThat(results.next(), is(true));
             assertThat(results.getString(2), is("ctid"));
        }
    }

    @Test
    public void test_insertsAreDetected() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().insertsAreDetected(ResultSet.TYPE_FORWARD_ONLY), is(false));
        }
    }

    @Test
    public void test_isCatalogAtStart() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().isCatalogAtStart(), is(true));
        }
    }

    @Test
    public void test_locatorsUpdateCopy() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().locatorsUpdateCopy(), is(true));
        }
    }

    @Test
    public void test_nullPlusNonNullIsNull() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().nullPlusNonNullIsNull(), is(true));
        }
    }

    @Test
    public void test_nullsAreSortedAtEnd() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().nullsAreSortedAtEnd(), is(false));
        }
    }

    @Test
    public void test_nullsAreSortedAtStart() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().nullsAreSortedAtStart(), is(false));
        }
    }

    @Test
    public void test_nullsAreSortedHigh() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().nullsAreSortedHigh(), is(true));
        }
    }

    @Test
    public void test_nullsAreSortedLow() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().nullsAreSortedLow(), is(false));
        }
    }

    @Test
    public void test_othersDeletesAreVisible() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().othersDeletesAreVisible(ResultSet.TYPE_FORWARD_ONLY), is(false));
        }
    }

    @Test
    public void test_othersInsertsAreVisible() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().othersInsertsAreVisible(ResultSet.TYPE_FORWARD_ONLY), is(false));
        }
    }

    @Test
    public void test_othersUpdatesAreVisible() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().othersUpdatesAreVisible(ResultSet.TYPE_FORWARD_ONLY), is(false));
        }
    }

    @Test
    public void test_ownDeletesAreVisible() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().ownDeletesAreVisible(ResultSet.TYPE_FORWARD_ONLY), is(true));
        }
    }

    @Test
    public void test_ownInsertsAreVisible() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().ownInsertsAreVisible(ResultSet.TYPE_FORWARD_ONLY), is(true));
        }
    }

    @Test
    public void test_ownUpdatesAreVisible() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().ownUpdatesAreVisible(ResultSet.TYPE_FORWARD_ONLY), is(true));
        }
    }

    @Test
    public void test_storesLowerCaseIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().storesLowerCaseIdentifiers(), is(true));
        }
    }

    @Test
    public void test_storesLowerCaseQuotedIdentifiers() throws Exception  {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().storesLowerCaseQuotedIdentifiers(), is(false));
        }
    }

    @Test
    public void test_storesMixedCaseIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().storesMixedCaseIdentifiers(), is(false));
        }
    }

    @Test
    public void test_storesMixedCaseQuotedIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().storesMixedCaseQuotedIdentifiers(), is(false));
        }
    }

    @Test
    public void test_storesUpperCaseIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().storesUpperCaseIdentifiers(), is(false));
        }
    }

    @Test
    public void test_storesUpperCaseQuotedIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().storesUpperCaseQuotedIdentifiers(), is(false));
        }
    }

    @Test
    public void test_supportsANSI92EntryLevelSQL() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsANSI92EntryLevelSQL(), is(true));
        }
    }

    @Test
    public void test_supportsANSI92FullSQL() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsANSI92FullSQL(), is(false));
        }
    }

    @Test
    public void test_supportsANSI92IntermediateSQL() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsANSI92IntermediateSQL(), is(false));
        }
    }

    @Test
    public void test_supportsAlterTableWithAddColumn() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsAlterTableWithAddColumn(), is(true));
        }
    }

    @Test
    public void test_supportsAlterTableWithDropColumn() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsAlterTableWithDropColumn(), is(true));
        }
    }

    @Test
    public void test_supportsBatchUpdates() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsBatchUpdates(), is(true));
        }
    }

    @Test
    public void test_supportsCatalogsInDataManipulation() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCatalogsInDataManipulation(), is(false));
        }
    }

    @Test
    public void test_supportsCatalogsInIndexDefinitions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCatalogsInIndexDefinitions(), is(false));
        }
    }

    @Test
    public void test_supportsCatalogsInPrivilegeDefinitions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCatalogsInPrivilegeDefinitions(), is(false));
        }
    }

    @Test
    public void test_supportsCatalogsInProcedureCalls() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCatalogsInProcedureCalls(), is(false));
        }
    }

    @Test
    public void test_supportsCatalogsInTableDefinitions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCatalogsInTableDefinitions(), is(false));
        }
    }

    @Test
    public void test_supportsColumnAliasing() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsColumnAliasing(), is(true));
        }
    }

    @Test
    public void test_supportsConvert() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsConvert(), is(false));
        }
    }

    @Test
    public void test_supportsConvertWithArgs() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsConvert(1, 1), is(false));
        }
    }

    @Test
    public void test_supportsCoreSQLGrammar() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCoreSQLGrammar(), is(false));
        }
    }

    @Test
    public void test_supportsCorrelatedSubqueries() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsCorrelatedSubqueries(), is(true));
        }
    }

    @Test
    public void test_supportsDataDefinitionAndDataManipulationTransactions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsDataDefinitionAndDataManipulationTransactions(), is(true));
        }
    }

    @Test
    public void test_supportsDataManipulationTransactionsOnly() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsDataManipulationTransactionsOnly(), is(false));
        }
    }

    @Test
    public void test_supportsDifferentTableCorrelationNames() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsDifferentTableCorrelationNames(), is(false));
        }
    }

    @Test
    public void test_supportsExpressionsInOrderBy() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsExpressionsInOrderBy(), is(true));
        }
    }

    @Test
    public void test_supportsExtendedSQLGrammar() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsExtendedSQLGrammar(), is(false));
        }
    }

    @Test
    public void test_supportsFullOuterJoins() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsFullOuterJoins(), is(true));
        }
    }

    @Test
    public void test_supportsGetGeneratedKeys() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsGetGeneratedKeys(), is(true));
        }
    }

    @Test
    public void test_supportsGroupBy() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsGroupBy(), is(true));
        }
    }

    @Test
    public void test_supportsGroupByBeyondSelect() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsGroupByBeyondSelect(), is(true));
        }
    }

    @Test
    public void test_supportsGroupByUnrelated() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsGroupByUnrelated(), is(true));
        }
    }

    @Test
    public void test_supportsIntegrityEnhancementFacility() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsIntegrityEnhancementFacility(), is(true));
        }
    }

    @Test
    public void test_supportsLikeEscapeClause() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsLikeEscapeClause(), is(true));
        }
    }

    @Test
    public void test_supportsLimitedOuterJoins() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsLimitedOuterJoins(), is(true));
        }
    }

    @Test
    public void test_supportsMinimumSQLGrammar() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsMinimumSQLGrammar(), is(true));
        }
    }

    @Test
    public void test_supportsMixedCaseIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsMixedCaseIdentifiers(), is(false));
        }
    }

    @Test
    public void test_supportsMixedCaseQuotedIdentifiers() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsMixedCaseQuotedIdentifiers(), is(true));
        }
    }

    @Test
    public void test_supportsMultipleOpenResults() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsMultipleOpenResults(), is(false));
        }
    }

    @Test
    public void test_supportsMultipleResultSets() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsMultipleResultSets(), is(true));
        }
    }

    @Test
    public void test_supportsMultipleTransactions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsMultipleTransactions(), is(true));
        }
    }

    @Test
    public void test_supportsNamedParameters() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsNamedParameters(), is(false));
        }
    }

    @Test
    public void test_supportsNonNullableColumns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsNonNullableColumns(), is(true));
        }
    }

    @Test
    public void test_supportsOpenCursorsAcrossCommit() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsOpenCursorsAcrossCommit(), is(false));
        }
    }

    @Test
    public void test_supportsOpenCursorsAcrossRollback() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsOpenCursorsAcrossRollback(), is(false));
        }
    }

    @Test
    public void test_supportsOpenStatementsAcrossCommit() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsOpenStatementsAcrossCommit(), is(true));
        }
    }

    @Test
    public void test_supportsOpenStatementsAcrossRollback() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsOpenStatementsAcrossRollback(), is(true));
        }
    }

    @Test
    public void test_supportsOrderByUnrelated() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsOrderByUnrelated(), is(true));
        }
    }

    @Test
    public void test_supportsOuterJoins() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsOuterJoins(), is(true));
        }
    }

    @Test
    public void test_supportsPositionedDelete() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsPositionedDelete(), is(false));
        }
    }

    @Test
    public void test_supportsPositionedUpdate() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsPositionedUpdate(), is(false));
        }
    }

    @Test
    public void test_supportsRefCursors() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsRefCursors(), is(true));
        }
    }

    @Test
    public void test_supportsResultSetConcurrency() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(
                conn.getMetaData().supportsResultSetConcurrency(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY),
                is(true)
            );
        }
    }

    @Test
    public void test_supportsResultSetHoldability() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsResultSetHoldability(ResultSet.HOLD_CURSORS_OVER_COMMIT), is(true));
        }
    }

    @Test
    public void test_supportsResultSetType() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsResultSetType(ResultSet.TYPE_FORWARD_ONLY), is(true));
        }
    }

    @Test
    public void test_supportsSavepoints() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSavepoints(), is(true));
        }
    }

    @Test
    public void test_supportsSchemasInDataManipulation() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSchemasInDataManipulation(), is(true));
        }
    }

    @Test
    public void test_supportsSchemasInIndexDefinitions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSchemasInIndexDefinitions(), is(true));
        }
    }

    @Test
    public void test_supportsSchemasInPrivilegeDefinitions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSchemasInPrivilegeDefinitions(), is(true));
        }
    }

    @Test
    public void test_supportsSchemasInProcedureCalls() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSchemasInProcedureCalls(), is(true));
        }
    }

    @Test
    public void test_supportsSchemasInTableDefinitions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSchemasInTableDefinitions(), is(true));
        }
    }

    @Test
    public void test_supportsSelectForUpdate() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSelectForUpdate(), is(true));
        }
    }

    @Test
    public void test_supportsSharding() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSharding(), is(false));
        }
    }

    @Test
    public void test_supportsStatementPooling() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsStatementPooling(), is(false));
        }
    }

    @Test
    public void test_supportsStoredFunctionsUsingCallSyntax() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsStoredFunctionsUsingCallSyntax(), is(true));
        }
    }

    @Test
    public void test_supportsStoredProcedures() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsStoredProcedures(), is(true));
        }
    }

    @Test
    public void test_supportsSubqueriesInComparisons() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSubqueriesInComparisons(), is(true));
        }
    }

    @Test
    public void test_supportsSubqueriesInExists() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSubqueriesInExists(), is(true));
        }
    }

    @Test
    public void test_supportsSubqueriesInIns() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSubqueriesInIns(), is(true));
        }
    }

    @Test
    public void test_supportsSubqueriesInQuantifieds() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsSubqueriesInQuantifieds(), is(true));
        }
    }

    @Test
    public void test_supportsTableCorrelationNames() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsTableCorrelationNames(), is(true));
        }
    }

    @Test
    public void test_supportsTransactionIsolationLevel() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsTransactionIsolationLevel(Connection.TRANSACTION_READ_UNCOMMITTED), is(true));
        }
    }

    @Test
    public void test_supportsTransactions() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsTransactions(), is(true));
        }
    }

    @Test
    public void test_supportsUnion() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsUnion(), is(true));
        }
    }

    @Test
    public void test_supportsUnionAll() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().supportsUnionAll(), is(true));
        }
    }

    @Test
    public void test_updatesAreDetected() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().updatesAreDetected(ResultSet.TYPE_FORWARD_ONLY), is(false));
        }
    }

    @Test
    public void test_usesLocalFilePerTable() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().usesLocalFilePerTable(), is(false));
        }
    }

    @Test
    public void test_usesLocalFiles() throws Exception {
        try (var conn = DriverManager.getConnection(URL)) {
            assertThat(conn.getMetaData().usesLocalFiles(), is(false));
        }
    }
}


