import json

from aiokafka import ConsumerRecord

from src.app.application.common.dto.recipe.recipe import RecipeEvent
from src.app.application.common.enums import OperationType
from src.app.application.models.recipe import Difficulty, Cuisine, Recipe


def parse_message(message: ConsumerRecord) -> RecipeEvent:
    data = json.loads(message.value.decode('utf-8'))
    key_data = json.loads(message.key.decode('utf-8'))

    operation_type = OperationType(data['op'])
    recipe_data = data['after']


    if operation_type == OperationType.DELETE:
        return RecipeEvent(
            id=key_data['id'],
            operation_type=OperationType.DELETE
        )
    recipe = Recipe(
        title=recipe_data['title'],
        ingredients=recipe_data['ingredients'],
        instructions=recipe_data['instructions'],
        cooking_time=recipe_data['cooking_time'],
        difficulty=Difficulty[recipe_data['difficulty'].upper()],
        cuisine=Cuisine[recipe_data['cuisine'].upper()]
    )
    recipe_event = RecipeEvent(
        id=key_data['id'],
        operation_type=operation_type,
        body=recipe,
    )
    return recipe_event