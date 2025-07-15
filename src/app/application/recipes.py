from typing import List

from src.app.application.common.dto.recipe.recipe import RecipeUpdateDto, RecipeResponse, RecipeDto, RecipeFilter

from src.app.application.common.dto.recipe.mappers import update_from_request, to_response_dto, to_recipe
from src.app.application.common.exceptions import NotFoundError
from src.app.application.protocols.database import UoW, AbstractSqlRecipeGateway, AbstractChromaRecipeGateway


def new_recipe(
    recipe_dto: RecipeDto,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> str:
    recipe = to_recipe(recipe_dto)
    gateway.create_recipe(recipe)
    uow.commit()
    return recipe.id

def search_recipe(
        input: str,
        gateway: AbstractChromaRecipeGateway
) -> List[RecipeResponse]:
    retrieved_recipes = gateway.search(input)
    response_recipes = [to_response_dto(recipe) for recipe in retrieved_recipes]
    return response_recipes

def find_recipe_by_id(
    recipe_id: str,
    gateway: AbstractSqlRecipeGateway
) -> RecipeResponse:
    recipe = gateway.find_recipe_by_id(recipe_id)
    if recipe is None:
        raise NotFoundError(f"Recipe with ID {recipe_id} not found")
    return to_response_dto(recipe)

def get_filtered_recipes(
    filters: RecipeFilter,
    gateway: AbstractSqlRecipeGateway
) -> List[RecipeResponse]:
    filtered_recipes = gateway.find_all(filters)
    response_list = [to_response_dto(r) for r in filtered_recipes]
    return response_list

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