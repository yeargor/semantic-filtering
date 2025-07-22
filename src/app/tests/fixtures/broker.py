from typing import AsyncGenerator, Any, Generator

import pytest
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from testcontainers.kafka import KafkaContainer

from src.app.adapters.kafka.consumer import KafkaConsumer


@pytest.fixture(scope="session")
def kafka_container() -> Generator[KafkaContainer, Any, None]:
    with KafkaContainer() as kafka:
        yield kafka

@pytest.fixture(scope="session")
def kafka_topic(kafka_container) -> None:
    topic_name = "topic"
    bootstrap_servers = kafka_container.get_bootstrap_server()
    print(f"Attempting to create Kafka topic '{topic_name}' on {bootstrap_servers}...")
    command = (
        f"kafka-topics.sh --create --topic {topic_name} "
        f"--bootstrap-server {bootstrap_servers} "
        "--partitions 1 --replication-factor 1"
    )
    try:
        kafka_container.exec(command)
    except:
        raise Exception

@pytest.fixture()
async def kafka_producer(kafka_container, kafka_topic) -> AsyncGenerator[AIOKafkaProducer, Any]:
    producer = AIOKafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server())
    await producer.start()
    yield producer
    await producer.stop()

@pytest.fixture()
async def consumer(kafka_container):
    consumer = AIOKafkaConsumer(
        "topic",
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        auto_offset_reset="earliest",
        group_id="test-group"
    )
    return consumer

@pytest.fixture()
async def kafka_consumer(consumer, recipe_handler) ->  AsyncGenerator[KafkaConsumer, Any]:
    consumer_wrapper = KafkaConsumer(consumer, recipe_handler)
    await consumer_wrapper.start()
    yield consumer_wrapper
    await consumer_wrapper.stop()