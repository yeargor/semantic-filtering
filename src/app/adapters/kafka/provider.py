import os

from aiokafka import AIOKafkaConsumer
from dishka import Provider, provide, Scope

from src.app.adapters.kafka.config import ConsumerConfig
from src.app.adapters.kafka.consumer import KafkaConsumer
from src.app.application.broker_handler import RecipeHandler
from src.app.application.protocols.consumer import AbstractConsumer

class KafkaProvider(Provider):
    @provide(scope=Scope.APP, provides=ConsumerConfig)
    def get_config(self) -> ConsumerConfig:
        raw_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "undefined")
        bootstrap_servers_list = [server.strip() for server in raw_servers.split(',')]
        kafka_topics_str = os.getenv("KAFKA_TOPICS", "recipe-updates.public.recipe")
        kafka_topics_list = [topic.strip() for topic in kafka_topics_str.split(',')]
        consumer_group_id = os.getenv("KAFKA_GROUP_ID", "default")

        return ConsumerConfig(
            kafka_topics_list,
            consumer_group_id=consumer_group_id,
            bootstrap_servers=bootstrap_servers_list
        )

    @provide(scope=Scope.APP)
    async def get_kafka_consumer(self, config: ConsumerConfig) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            *config.topics,
            bootstrap_servers=config.bootstrap_servers,
            auto_offset_reset="earliest"
        )

    @provide(scope=Scope.APP, provides=AbstractConsumer)
    async def get_kafka_consumer_wrapper(
            self,
            raw_aiokafka_consumer: AIOKafkaConsumer,
            handler: RecipeHandler,
    ) -> KafkaConsumer:
        return KafkaConsumer(raw_aiokafka_consumer,handler)