package io.crate;

import org.hibernate.dialect.Dialect;
import org.hibernate.metamodel.mapping.EmbeddableMappingType;
import org.hibernate.metamodel.spi.RuntimeModelCreationContext;
import org.hibernate.sql.ast.spi.SqlAppender;
import org.hibernate.type.SqlTypes;
import org.hibernate.type.descriptor.jdbc.AggregateJdbcType;
import org.hibernate.type.descriptor.jdbc.JsonJdbcType;

/**
 * custom type for crate json
 *
 * @author mackerl
 */
public class CrateDBJsonJdbcType extends JsonJdbcType {

    public static final CrateDBJsonJdbcType JSON_INSTANCE = new CrateDBJsonJdbcType(null);

    public CrateDBJsonJdbcType(EmbeddableMappingType embeddableMappingType) {
        super(embeddableMappingType);
    }

    @Override
    public int getDdlTypeCode() {
        return SqlTypes.JSON;
    }

    @Override
    public AggregateJdbcType resolveAggregateJdbcType(EmbeddableMappingType mappingType,
                                                      String sqlType,
                                                      RuntimeModelCreationContext creationContext) {
        return new CrateDBJsonJdbcType(mappingType);
    }

    @Override
    public void appendWriteExpression(String writeExpression, SqlAppender appender, Dialect dialect) {
        appender.append(writeExpression);
    }
}