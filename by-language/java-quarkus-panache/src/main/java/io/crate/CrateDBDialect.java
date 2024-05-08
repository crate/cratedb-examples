package io.crate;

import org.hibernate.boot.model.TypeContributions;
import org.hibernate.dialect.DatabaseVersion;
import org.hibernate.dialect.PostgreSQLDialect;
import org.hibernate.dialect.sequence.NoSequenceSupport;
import org.hibernate.dialect.sequence.SequenceSupport;
import org.hibernate.service.ServiceRegistry;
import org.hibernate.type.descriptor.jdbc.spi.JdbcTypeRegistry;
import org.hibernate.type.descriptor.sql.internal.DdlTypeImpl;
import org.hibernate.type.descriptor.sql.spi.DdlTypeRegistry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.hibernate.type.SqlTypes.JSON;
import static org.hibernate.type.SqlTypes.TIMESTAMP;
import static org.hibernate.type.SqlTypes.TIMESTAMP_WITH_TIMEZONE;
import static org.hibernate.type.SqlTypes.NUMERIC;

/**
 * extends postgres sql dialect with crate specialities and also cover
 * limitations
 *
 * @author mackerl
 */
public class CrateDBDialect extends PostgreSQLDialect {

    private static final Logger log = LoggerFactory.getLogger(CrateDBDialect.class);

    public CrateDBDialect() {
        super(DatabaseVersion.make(14));
        log.info("creating crate dialect");
    }

    @Override
    public SequenceSupport getSequenceSupport() {
        return NoSequenceSupport.INSTANCE;
    }

    @Override
    protected void registerColumnTypes(TypeContributions typeContributions, ServiceRegistry serviceRegistry) {
        super.registerColumnTypes(typeContributions, serviceRegistry);
        final DdlTypeRegistry ddlTypeRegistry = typeContributions.getTypeConfiguration().getDdlTypeRegistry();

        // Prefer object if possible
        ddlTypeRegistry.addDescriptor(new DdlTypeImpl(JSON, "OBJECT(DYNAMIC)", this));
    }

    @Override
    protected String columnType(int sqlTypeCode) {
        switch (sqlTypeCode) {
            case TIMESTAMP:
                return "timestamp"; // TODO does not support precision for timestamps
            case TIMESTAMP_WITH_TIMEZONE:
                return "timestamp with time zone"; // TODO does not support precision for timestamps
            case NUMERIC:
                return "double"; // TODO bigdecimal not supported
            case JSON:
                return "OBJECT(DYNAMIC)";
            default:
                return super.columnType(sqlTypeCode);
        }
    }

    @Override
    public String getArrayTypeName(String javaElementTypeName, String elementTypeName, Integer maxLength) {
        return supportsStandardArrays() ? " array(" + elementTypeName + ") " : null;
    }

    @Override
    public void contribute(TypeContributions typeContributions, ServiceRegistry serviceRegistry) {
        super.contributeTypes(typeContributions, serviceRegistry);

        contributeCrateTypes(typeContributions);
    }

    private void contributeCrateTypes(TypeContributions typeContributions) {
        final JdbcTypeRegistry jdbcTypeRegistry = typeContributions.getTypeConfiguration().getJdbcTypeRegistry();

        jdbcTypeRegistry.addDescriptor(CrateDBJsonJdbcType.JSON_INSTANCE);

    }

    @Override
    public String getQuerySequencesString() {
        return null;
    }

    @Override
    public boolean supportsIfExistsBeforeTableName() {
        return true;
    }

    @Override
    public boolean supportsIfExistsBeforeTypeName() {
        return false;
    }

    @Override
    public boolean supportsIfExistsBeforeConstraintName() {
        return false;
    }

    @Override
    public boolean supportsIfExistsAfterAlterTable() {
        return false;
    }

    @Override
    public boolean supportsAlterColumnType() {
        return false;
    }

    @Override
    public String getAlterColumnTypeString(String columnName, String columnType, String columnDefinition) {
        return null;
    }

}
