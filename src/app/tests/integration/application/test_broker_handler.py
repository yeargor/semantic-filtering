import asyncio
import json

from aiokafka import AIOKafkaProducer

from src.app.adapters.kafka.consumer import KafkaConsumer
from src.app.application.broker_handler import RecipeHandler
from src.app.tests.mocks.gateway import RecipeChromaGatewayMock

async def test_handler_receives_create_event_recipe_created(
        kafka_producer: AIOKafkaProducer,
        kafka_consumer: KafkaConsumer,
        chroma_gateway: RecipeChromaGatewayMock,
        recipe_handler: RecipeHandler
):
    test_topic = "topic"
    message_id = "dc161d07-aad1-4309-a315-b323f13e9ba1"
    msg_key_data = {"id": message_id}
    msg_key_bytes = json.dumps(msg_key_data).encode('utf-8')
    msg_value_data = {
        "after": {
            "id": message_id,
            "title": "new_recipe",
            "ingredients": ["string"],
            "instructions": "string",
            "cooking_time": 0,
            "difficulty": "EASY",
            "cuisine": "ITALIAN"
        },
        "op": "c"
    }
    msg_value_bytes = json.dumps(msg_value_data).encode('utf-8')
    await kafka_producer.send_and_wait(test_topic, msg_value_bytes, key=msg_key_bytes)
    await asyncio.sleep(2)
    assert len(chroma_gateway.recipes) == 1
    created_recipe = chroma_gateway.recipes[0]
    assert created_recipe.title == "new_recipe"