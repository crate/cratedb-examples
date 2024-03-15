import json
import logging
import os
import sched
import time
import functools

import requests

from kafka import KafkaProducer

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

CRATEDB_HOST = os.getenv('CRATEDB_HOST', 'crate') + os.getenv('CRATEDB_PORT', '4200')
API_KEY = os.getenv('WEATHER_PRODUCER_API_KEY')
CITY = os.getenv('WEATHER_PRODUCER_CITY')

WEATHER_URI = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no'

RUN_EVERY_SECONDS = int(os.getenv('WEATHER_PRODUCER_FETCH_EVERY_SECONDS', 5))
BOOTSTRAP_SERVER = os.getenv('WEATHER_PRODUCER_KAFKA_BOOTSTRAP_SERVER')
KAFKA_TOPIC = os.getenv('WEATHER_PRODUCER_KAFKA_TOPIC')

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER,
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))


@functools.cache
def mocked_fetch_weather_data():
    with open('example.json') as f:
        return json.loads(f.read())


def fetch_weather_data(api_uri) -> dict:
    response = requests.get(api_uri)
    response.raise_for_status()
    return response.json()


def send_to_kafka(topic: str, producer) -> None:
    data = fetch_weather_data(WEATHER_URI)
    producer.send(topic, value=data)
    producer.flush()


def schedule_every(seconds, func, scheduler):
    # schedule the next call first
    scheduler.enter(seconds, 1, schedule_every, (RUN_EVERY_SECONDS, func, scheduler))
    func()


def main():
    try:
        produce_weather_data = functools.partial(send_to_kafka, KAFKA_TOPIC, producer)
        logger.debug(f'Starting scheduler, will run every {RUN_EVERY_SECONDS}(s)')
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(
            RUN_EVERY_SECONDS,
            1,
            schedule_every,
            (RUN_EVERY_SECONDS, produce_weather_data, scheduler)
        )
        scheduler.run()

    except KeyboardInterrupt:
        logger.info('Exit: KeyboardInterrupt')


if __name__ == '__main__':
    main()
