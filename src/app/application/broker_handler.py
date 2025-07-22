from src.app.application.common.dto.recipe.recipe import RecipeEvent
from src.app.application.common.enums import OperationType
from src.app.application.protocols.database import AbstractChromaRecipeGateway


class RecipeHandler:
    def __init__(
            self,
            gateway: AbstractChromaRecipeGateway
    ):
        self.gateway = gateway

    async def handle_recipe_update(
            self,
            recipe_event: RecipeEvent
    ):
        match recipe_event.operation_type:
            case OperationType.CREATE:
                await self.gateway.create_recipe(recipe_event.body)
            case OperationType.UPDATE:
                await self.gateway.update_recipe(recipe_event.id, recipe_event.body)
            case OperationType.DELETE:
                await self.gateway.delete_recipe(recipe_event.id)