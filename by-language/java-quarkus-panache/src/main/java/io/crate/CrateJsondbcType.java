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
public class CrateJsondbcType extends JsonJdbcType {

    public static final CrateJsondbcType JSON_INSTANCE = new CrateJsondbcType(null);

    public CrateJsondbcType(EmbeddableMappingType embeddableMappingType) {
        super(embeddableMappingType);
    }

    @Override
    public int getDdlTypeCode() {
        return SqlTypes.JSON;
    }

    @Override
    public AggregateJdbcType resolveAggregateJdbcType(EmbeddableMappingType mappingType, String sqlType,
            RuntimeModelCreationContext creationContext) {
        return new CrateJsondbcType(mappingType);
    }

    @Override
    public void appendWriteExpression(String writeExpression, SqlAppender appender, Dialect dialect) {
        appender.append(writeExpression);

    }
}