from typing import List

from src.app.application.common.dto.recipe.recipe import RecipeUpdateDto, RecipeResponse, RecipeDto, RecipeFilter

from src.app.application.common.dto.recipe.mappers import update_from_request, to_response_dto, to_recipe
from src.app.application.common.exceptions import NotFoundError
from src.app.application.protocols.database import UoW, AbstractSqlRecipeGateway, AbstractChromaRecipeGateway


async def new_recipe(
    recipe_dto: RecipeDto,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> str:
    recipe = to_recipe(recipe_dto)
    await gateway.create_recipe(recipe)
    await uow.commit()
    return recipe.id

async def search_recipe(
        input: str,
        gateway: AbstractChromaRecipeGateway
) -> List[RecipeResponse]:
    retrieved_recipes = await gateway.search(input)
    response_recipes = [to_response_dto(recipe) for recipe in retrieved_recipes]
    return response_recipes

async def find_recipe_by_id(
    recipe_id: str,
    gateway: AbstractSqlRecipeGateway
) -> RecipeResponse:
    recipe = await gateway.find_recipe_by_id(recipe_id)
    if recipe is None:
        raise NotFoundError(f"Recipe with ID {recipe_id} not found")
    return to_response_dto(recipe)

async def get_filtered_recipes(
    filters: RecipeFilter,
    gateway: AbstractSqlRecipeGateway
) -> List[RecipeResponse]:
    filtered_recipes = await gateway.find_all(filters)
    response_list = [to_response_dto(r) for r in filtered_recipes]
    return response_list

async def update_recipe(
    recipe_id: str,
    recipe_dto: RecipeUpdateDto,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> RecipeResponse:
    recipe = await gateway.find_recipe_by_id(recipe_id)
    if recipe is None:
        raise NotFoundError(f"Recipe with ID {recipe_id} not found")
    update_from_request(target=recipe, source=recipe_dto)
    await gateway.update_recipe(recipe)
    await uow.commit()
    return to_response_dto(recipe)

async def delete_recipe(
    recipe_id: str,
    gateway: AbstractSqlRecipeGateway,
    uow: UoW
) -> None:
    await gateway.delete_recipe(recipe_id)
    await uow.commit()