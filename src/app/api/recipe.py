from uuid import UUID
from typing import Annotated, List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from src.app.api.docs import tags_metadata
from src.app.application.common.dto.message.message import MessageDTO
from src.app.application.common.dto.recipe.recipe import RecipeDto, RecipeCreateResponse, RecipeResponse, \
    RecipeUpdateDto, RecipeFilter
from src.app.application.protocols.database import AbstractSqlRecipeGateway, UoW, AbstractChromaRecipeGateway
from src.app.application.recipes import new_recipe, find_recipe_by_id, update_recipe, delete_recipe, \
    get_filtered_recipes, search_recipe

recipe_router = APIRouter(prefix="/recipe")


@recipe_router.post('',tags=["create"])
@inject
async def create(
        recipe_dto: RecipeDto,
        gateway: FromDishka[AbstractSqlRecipeGateway],
        uow: FromDishka[UoW]
) -> RecipeCreateResponse:
    """
    Create new recipes. This endpoint allows you to add new recipe entries to the database.
    Returns: Created Recipe's Id
    """
    recipe_id = await new_recipe(
        recipe_dto,
        gateway,
        uow
    )
    return RecipeCreateResponse(recipe_id)

@recipe_router.get('/{recipe_id}', tags=["get"])
@inject
async def get(
        recipe_id: UUID,
        gateway: FromDishka[AbstractSqlRecipeGateway]
) -> RecipeResponse:
    """
    Retrieve a single recipe by its unique ID. Use this to fetch detailed information about a specific recipe.
    Returns: Founded Recipe
    """
    recipe = await find_recipe_by_id(
        str(recipe_id),
        gateway
    )
    return recipe

@recipe_router.patch('/{recipe_id}', tags=["update"])
@inject
async def update(
        recipe_id: UUID,
        recipe_request: RecipeUpdateDto,
        gateway: FromDishka[AbstractSqlRecipeGateway],
        uow: FromDishka[UoW]
) -> RecipeResponse:
    """
    Update an existing recipe. This endpoint allows for modification of recipe details using its ID.
    Returns: Updated Recipe
    """
    updated_recipe = await update_recipe(
        str(recipe_id),
        recipe_request,
        gateway,
        uow
    )
    return updated_recipe

@recipe_router.delete('/{recipe_id}', tags=["delete"])
@inject
async def delete(
    recipe_id: UUID,
    gateway: FromDishka[AbstractSqlRecipeGateway],
    uow: FromDishka[UoW]
) -> None:
    """
    Delete a recipe by its unique ID. This action removes a recipe from the database.
    Returns: None
    """
    return await delete_recipe(
        str(recipe_id),
        gateway,
        uow
    )

@recipe_router.post('/search', tags=["semantic_search"])
@inject
async def semantic_search(
        message: MessageDTO,
        gateway: FromDishka[AbstractChromaRecipeGateway],
) -> List[RecipeResponse]:
    """
    Perform a semantic search for recipes. This endpoint uses natural language queries to find relevant recipes.
    Returns: List of relevant recipes
    """
    return await search_recipe(message.data, gateway)

@recipe_router.get('',tags=["get_all"])
@inject
async def get_all(
    gateway: FromDishka[AbstractSqlRecipeGateway],
    filters: Annotated[RecipeFilter, Query()]
) -> List[RecipeResponse]:
    """
    Retrieve a list of recipes, with optional filtering. Returns list of recipes based on inclusion/exclusion of ingredients.
    Returns: List of recipes based on inclusion/exclusion of ingredients
    """
    return await get_filtered_recipes(filters, gateway)
