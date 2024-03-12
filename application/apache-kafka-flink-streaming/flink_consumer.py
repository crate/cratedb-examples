import os
import logging

from pathlib import Path

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions, JdbcExecutionOptions
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s',
    level=logging.DEBUG
)

JARS_PATH = Path(__file__).parent / 'jars'

KAFKA_BOOTSTRAP_SERVER = os.getenv('FLINK_CONSUMER_BOOTSTRAP_SERVER')
KAFKA_TOPIC = os.getenv('FLINK_CONSUMER_KAFKA_TOPIC')
CRATEDB_PG_URI = os.getenv('FLINK_CONSUMER_CRATEDB_PG_URI', 'jdbc:postgresql://localhost:5432/crate')
CRATEDB_USER = os.getenv('FLINK_CONSUMER_CRATE_USER')
CRATEDB_PASSWORD = os.getenv('FLINK_CONSUMER_CRATE_PASSWORD')


def kafka_to_cratedb(env: StreamExecutionEnvironment):
    row_type_info = Types.ROW_NAMED(['location', 'current'], [Types.STRING(), Types.STRING()])
    json_format = JsonRowDeserializationSchema.builder().type_info(row_type_info).build()

    # Consumes data from Kafka.
    kafka_consumer = FlinkKafkaConsumer(
        topics=KAFKA_TOPIC,
        deserialization_schema=json_format,
        properties={'bootstrap.servers': f'{KAFKA_BOOTSTRAP_SERVER}:9092'}
    )
    kafka_consumer.set_start_from_latest()

    ds = env.add_source(kafka_consumer, source_name='kafka')

    # Writes data to cratedb.
    ds.add_sink(
        JdbcSink.sink(
            "insert into doc.weather_flink_sink (location, current) values (?, ?)",
            row_type_info,
            JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url(CRATEDB_PG_URI)
            .with_driver_name('org.postgresql.Driver')
            .with_user_name(CRATEDB_USER)
            .with_password(CRATEDB_PASSWORD)
            .build(),
            JdbcExecutionOptions.builder()
            .with_batch_interval_ms(1000)
            .with_batch_size(200)
            .with_max_retries(5)
            .build()
        )
    )
    env.execute()


if __name__ == '__main__':
    env = StreamExecutionEnvironment.get_execution_environment()
    jars = list(map(lambda x: 'file://' + str(x), (JARS_PATH.glob('*.jar'))))
    env.add_jars(*jars)

    logging.info("Reading data from kafka")
    kafka_to_cratedb(env)
