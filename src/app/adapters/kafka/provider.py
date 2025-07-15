from aiokafka import AIOKafkaConsumer
from dishka import Provider, provide, Scope

from src.app.adapters.kafka.consumer import KafkaConsumer
from src.app.application.broker_handler import RecipeHandler
from src.app.application.protocols.consumer import AbstractConsumer

class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_kafka_consumer(self) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            "recipe-updates.public.recipe",
            bootstrap_servers='localhost:29092'
        )

    @provide(scope=Scope.APP, provides=AbstractConsumer)
    async def get_kafka_consumer_wrapper(
            self,
            raw_aiokafka_consumer: AIOKafkaConsumer,
            handler: RecipeHandler,
    ) -> KafkaConsumer:
        kafka_wrapper_instance = KafkaConsumer(raw_aiokafka_consumer,handler)
        await kafka_wrapper_instance.start()
        yield kafka_wrapper_instance
        await kafka_wrapper_instance.stop()