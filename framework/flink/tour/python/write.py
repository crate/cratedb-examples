import dataclasses
import logging

from pathlib import Path

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions, JdbcExecutionOptions


logger = logging.getLogger(__name__)

JARS_PATH = Path(__file__).parent / 'jars'


@dataclasses.dataclass
class Person:
    name: str
    age: int


def main():

    env = StreamExecutionEnvironment.get_execution_environment()
    jars = list(map(lambda x: 'file://' + str(x), (JARS_PATH.glob('*.jar'))))
    env.add_jars(*jars)

    # Define source data.
    ds = env.from_collection([
        Person("Fred", 35),
        Person("Wilma", 35),
        Person("Pebbles", 2),
    ])

    # Define CrateDB as data sink.
    row_type_info = Types.ROW_NAMED(['name', 'age'], [Types.STRING(), Types.INT()])
    ds.add_sink(
        JdbcSink.sink(
            "INSERT INTO person (name, age) VALUES (?, ?)",
            row_type_info,

            # FIXME (Flink >= 1.19): java.lang.NoSuchMethodException: org.apache.flink.connector.jdbc.internal.JdbcOutputFormat.createRowJdbcStatementBuilder

            # This is due to a bug in the python Flink library. In `flink-connector-jdbc` v3.1,
            # the `JdbcOutputFormat` was renamed to `RowJdbcOutputFormat`. This change has up till
            # now not been implemented in the python Flink library.
            # https://stackoverflow.com/questions/78960829/java-lang-nosuchmethodexception-in-python-flink-jdbc

            # As you see, java `JdbcSink` connector class has different shape from Python `JdbcSink` connector.
            # In Java code, `jdbcSink` object is generated from `JdbcSinkBuilder` class, but in Python it is not.
            # I think these errors are due to API version mismatch. Any idea to solve these errors?
            # https://stackoverflow.com/questions/79604252/issue-with-pyflink-api-code-for-inserting-data-into-sql

            JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url('jdbc:postgresql://localhost:5432/crate')
            .with_driver_name('org.postgresql.Driver')
            .with_user_name("crate")
            .with_password("crate")
            .build(),
            JdbcExecutionOptions.builder()
            .with_batch_interval_ms(1000)
            .with_batch_size(200)
            .with_max_retries(5)
            .build()
        )
    )

    # Execute pipeline.
    env.execute()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s',
        level=logging.DEBUG
    )

    logger.info("Start")
    main()
    logger.info("Ready")
