from src.app.application.common.dto.recipe.recipe import RecipeUpdateDto, RecipeResponse, RecipeDto

from src.app.application.common.dto.recipe.mappers import update_from_request, to_response_dto, to_recipe
from src.app.application.common.exceptions import NotFoundError
from src.app.application.protocols.database import UoW, AbstractSqlRecipeGateway


def new_recipe(
    recipe_dto: RecipeDto,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> str:
    recipe = to_recipe(recipe_dto)
    gateway.create_recipe(recipe)
    uow.commit()
    return recipe.id

def find_recipe_by_id(
    recipe_id: str,
    gateway: AbstractSqlRecipeGateway
) -> RecipeResponse:
    recipe = gateway.find_recipe_by_id(recipe_id)
    if recipe is None:
        raise NotFoundError(f"Recipe with ID {recipe_id} not found")
    return to_response_dto(recipe)

def update_recipe(
    recipe_id: str,
    recipe_dto: RecipeUpdateDto,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> RecipeResponse:
    recipe = gateway.find_recipe_by_id(recipe_id)
    if recipe is None:
        raise NotFoundError(f"Recipe with ID {recipe_id} not found")
    update_from_request(target=recipe, source=recipe_dto)
    gateway.update_recipe(recipe)
    uow.commit()
    return to_response_dto(recipe)

def delete_recipe(
    recipe_id: str,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> None:
    gateway.delete_recipe(recipe_id)
    uow.commit()