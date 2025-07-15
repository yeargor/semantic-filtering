import asyncio
from asyncio import Task

from aiokafka import AIOKafkaConsumer

from src.app.adapters.kafka.exceptions import KafkaConsumerError
from src.app.adapters.kafka.parser import parse_message
from src.app.application.broker_handler import RecipeHandler
from src.app.application.protocols.consumer import AbstractConsumer


class KafkaConsumer(AbstractConsumer):
    def __init__(
            self,
            consumer: AIOKafkaConsumer,
            handler: RecipeHandler,
    ):
        self.consumer = consumer
        self.handler = handler
        self._consume_task: Task | None = None

    async def start(self):
        await self.consumer.start()
        self._consume_task = asyncio.create_task(self.consume())

    async def consume(self):
        try:
            async for message in self.consumer:
                print(f'{message} \n')
                recipe_event = parse_message(message)
                await self.handler.handle_recipe_update(recipe_event)
        except Exception as e:
            raise KafkaConsumerError(e) from e

    async def stop(self):
        if self._consume_task:
            self._consume_task.cancel()
        if self.consumer:
            await self.consumer.stop()
            self.consumer = None