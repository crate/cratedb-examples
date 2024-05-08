package io.crate;

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import io.quarkus.hibernate.orm.panache.PanacheEntityBase;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.transaction.Transactional;

@Entity
public class MyEntity extends PanacheEntityBase { // using PanacheEntityBase instead of PanacheEntity as this has a
                                                  // Sequence ID
    @Id
    @Column(updatable = false, nullable = false, length = 36)
    public String myUUId; // using uuid as sequence replacement

    /**
     * demonstrate usage of JSON as Object(dynamic) -> see dialect
     */
    @JdbcTypeCode(SqlTypes.JSON)
    @Column
    public Map<String, String> key2Value = new HashMap<>();
    /**
     * demonstrate usage of timestamp with timezone
     */
    @Column
    public Instant timestamp = Instant.now();

    // TODO Bigdecimal not yet supported
    @Column(name = "\"value\"")
    public Long myValue;

    /**
     * demonstrates usage of array type
     */
    @Column
    public List<String> myArray = new ArrayList<>();

    @PrePersist
    /**
     * automatically creates a unique UUID as primary key.
     */
    private void ensureThereIsAnId() {
        if (isNullOrEmpty(myUUId)) {
            this.myUUId = UUID.randomUUID().toString();
        }
    }

    @Override
    public String toString() {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.registerModule(new JavaTimeModule());
            return objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(this);
        } catch (final Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Transactional
    /**
     * Crate DB does not support transactions - however for JPA this is required so
     * that the data is persisted.
     * As CrateDB does not support transactions, the only effect of this command is
     * to close all existing cursors WITHOUT HOLD in the current session.
     */
    public static void populateWithData(int numberOfEntitesToCreate) {

        for (int i = 1; i <= numberOfEntitesToCreate; i++) {
            MyEntity entity = new MyEntity();

            entity.key2Value.put("key" + i, "value" + i);
            entity.key2Value.put("key" + (i + 1), "value" + (i + 1));

            entity.myValue = (long) i;

            entity.myArray.add("item1");
            entity.myArray.add("item2");
            entity.myArray.add("item3");

            entity.persist();
        }
    }

    private boolean isNullOrEmpty(String s) {
        return s == null || s.isEmpty();
    }
}
