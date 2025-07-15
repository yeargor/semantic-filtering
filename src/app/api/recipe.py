from uuid import UUID
from typing import Annotated, List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query

from src.app.application.common.dto.message.message import MessageDTO
from src.app.application.common.dto.recipe.recipe import RecipeDto, RecipeCreateResponse, RecipeResponse, \
    RecipeUpdateDto, RecipeFilter
from src.app.application.protocols.database import AbstractSqlRecipeGateway, UoW, AbstractChromaRecipeGateway
from src.app.application.recipes import new_recipe, find_recipe_by_id, update_recipe, delete_recipe, \
    get_filtered_recipes, search_recipe

recipe_router = APIRouter(prefix="/recipe")

@recipe_router.post('')
@inject
async def create(
        recipe_dto: RecipeDto,
        gateway: FromDishka[AbstractSqlRecipeGateway],
        uow: FromDishka[UoW]
) -> RecipeCreateResponse:
    recipe_id = await new_recipe(
        recipe_dto,
        gateway,
        uow
    )
    return RecipeCreateResponse(recipe_id)

@recipe_router.post('/search')
@inject
async def semantic_search(
        message: MessageDTO,
        gateway: FromDishka[AbstractChromaRecipeGateway],
) -> List[RecipeResponse]:
    return await search_recipe(message.data, gateway)

@recipe_router.get('')
@inject
async def get_all(
    gateway: FromDishka[AbstractSqlRecipeGateway],
    filters: Annotated[RecipeFilter, Query()]
) -> List[RecipeResponse]:
    return await get_filtered_recipes(filters, gateway)

@recipe_router.get('/{recipe_id}')
@inject
async def get(
        recipe_id: UUID,
        gateway: FromDishka[AbstractSqlRecipeGateway]
) -> RecipeResponse:
    recipe = await find_recipe_by_id(
        str(recipe_id),
        gateway
    )
    return recipe

@recipe_router.patch('/{recipe_id}')
@inject
async def update(
        recipe_id: UUID,
        recipe_request: RecipeUpdateDto,
        gateway: FromDishka[AbstractSqlRecipeGateway],
        uow: FromDishka[UoW]
) -> RecipeResponse:
    updated_recipe = await update_recipe(
        str(recipe_id),
        recipe_request,
        gateway,
        uow
    )
    return updated_recipe

@recipe_router.delete('/{recipe_id}')
@inject
async def delete(
    recipe_id: UUID,
    gateway: FromDishka[AbstractSqlRecipeGateway],
    uow: FromDishka[UoW]
) -> None:
    return await delete_recipe(
        str(recipe_id),
        gateway,
        uow
    )