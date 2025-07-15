from src.app.application.common.dto.recipe.recipe import RecipeEvent
from src.app.application.common.enums import OperationType
from src.app.application.protocols.database import AbstractChromaRecipeGateway

class RecipeHandler:
    def __init__(
            self,
            gateway: AbstractChromaRecipeGateway
    ):
        self.gateway = gateway

    def handle_recipe_update(
            self,
            recipe_event: RecipeEvent
    ):
        print(f"Received recipe_event in application: {recipe_event} \n")
        match recipe_event.operation_type:
            case OperationType.CREATE:
                print("c was called")
                self.gateway.create_recipe(recipe_event.body)
            case OperationType.UPDATE:
                print("u was called")
                self.gateway.update_recipe(recipe_event.id, recipe_event.body)
            case OperationType.DELETE:
                print("d was called")
                self.gateway.delete_recipe(recipe_event.id)