// Write to CrateDB using Apache Flink.
// Invoke: uvx crash -c 'CREATE TABLE person (name STRING, age INT);'
// Invoke: gradle run write
// Source: https://github.com/crate/cratedb-examples/blob/main/framework/flink/tour/java/write.java

// https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/datastream/jdbc/#full-example

import org.apache.flink.connector.jdbc.*;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class write {

    public static void main(String[] args) throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Define source data.
        env.fromElements(
            new Person("Fred", 35),
            new Person("Wilma", 35),
            new Person("Pebbles", 2)

        // Define CrateDB as data sink.
        ).addSink(
            JdbcSink.sink(
                "INSERT INTO person (name, age) VALUES (?, ?)",
                (statement, person) -> {
                    statement.setString(1, person.name);
                    statement.setInt(2, person.age);
                },
                JdbcExecutionOptions.builder()
                    .withBatchSize(1000)
                    .withBatchIntervalMs(200)
                    .withMaxRetries(5)
                    .build(),
                new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                    .withUrl("jdbc:postgresql://localhost:5432/doc?sslmode=disable")
                    .withDriverName("org.postgresql.Driver")
                    .withUsername("crate")
                    .withPassword("crate")
                    .build()
            ));

        // Execute pipeline.
        env.execute();
    }

    public static class Person {
        public String name;
        public Integer age;
        public Person() {}
        public Person(String name, Integer age) {
            this.name = name;
            this.age = age;
        }
    }

}
