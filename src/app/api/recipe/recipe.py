from uuid import UUID
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.app.application.common.dto.recipe.recipe import RecipeDto, RecipeCreateResponse, RecipeResponse, \
    RecipeUpdateDto
from src.app.application.protocols.database import AbstractSqlRecipeGateway, UoW
from src.app.application.recipes import new_recipe, find_recipe_by_id, update_recipe, delete_recipe

recipe_router = APIRouter(prefix="/recipe")

@recipe_router.post('')
@inject
def create(
        recipe_dto: RecipeDto,
        gateway: FromDishka[AbstractSqlRecipeGateway],
        uow: FromDishka[UoW]
) -> RecipeCreateResponse:
    recipe_id = new_recipe(
        recipe_dto,
        gateway,
        uow
    )
    return RecipeCreateResponse(recipe_id)

@recipe_router.get('/{recipe_id}')
@inject
def get(
        recipe_id: UUID,
        gateway: FromDishka[AbstractSqlRecipeGateway]
) -> RecipeResponse:
    recipe = find_recipe_by_id(
        str(recipe_id),
        gateway
    )
    return recipe

@recipe_router.patch('/{recipe_id}')
@inject
def update(
        recipe_id: UUID,
        recipe_request: RecipeUpdateDto,
        gateway: FromDishka[AbstractSqlRecipeGateway],
        uow: FromDishka[UoW]
) -> RecipeResponse:
    updated_recipe = update_recipe(
        str(recipe_id),
        recipe_request,
        gateway,
        uow
    )
    return updated_recipe

@recipe_router.delete('/{recipe_id}')
@inject
def delete(
    recipe_id: str,
    gateway: FromDishka[AbstractSqlRecipeGateway],
    uow: FromDishka[UoW]
) -> None:
    return delete_recipe(
        recipe_id,
        gateway,
        uow
    )