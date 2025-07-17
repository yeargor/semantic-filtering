import pytest

from src.app.application.common.dto.recipe.recipe import RecipeDto, RecipeFilter
from src.app.application.common.exceptions import NotFoundError
from src.app.application.models.recipe import Cuisine, Difficulty, Recipe
from src.app.application.recipes import new_recipe, find_recipe_by_id, get_filtered_recipes
from src.app.tests.mocks.gateway import RecipeSqlGatewayMock
from src.app.tests.mocks.uow import UowMock

@pytest.fixture
def recipes() -> list[Recipe]:
    recipes: list[Recipe] = [
        Recipe(
            title="First recipe",
            ingredients=["onion", "pepper"],
            instructions="Some instructions",
            cooking_time=0,
            difficulty=Difficulty.EASY,
            cuisine=Cuisine.FRENCH
        ),
        Recipe(
            title="Second recipe",
            ingredients=["cheese", "butter"],
            instructions="Some instructions",
            cooking_time=0,
            difficulty=Difficulty.EASY,
            cuisine=Cuisine.FRENCH
        )
    ]
    return recipes

@pytest.fixture
def recipe_dto() -> RecipeDto:
    return RecipeDto(
        title = "First recipe",
        ingredients = ["onion", "pepper"],
        instructions = "Some instructions",
        cooking_time = 0,
        difficulty = Difficulty.EASY,
        cuisine = Cuisine.FRENCH
    )

@pytest.mark.asyncio
async def test_create_user_user_created(recipe_dto: RecipeDto, sql_gateway: RecipeSqlGatewayMock, uow: UowMock) -> None:
    recipe_id = await new_recipe(recipe_dto, sql_gateway, uow)
    recipe = sql_gateway.recipes[recipe_id]

    assert recipe.id == recipe_id

@pytest.mark.asyncio
async def test_find_recipe_by_id_recipe_found(recipe_dto, sql_gateway: RecipeSqlGatewayMock, uow: UowMock) -> None:
    recipe_id = await new_recipe(recipe_dto, sql_gateway, uow)
    founded_recipe = await find_recipe_by_id(recipe_id, sql_gateway)
    assert founded_recipe.title == recipe_dto.title

@pytest.mark.asyncio
async def test_find_recipe_by_id_recipe_not_found(recipe_dto, sql_gateway: RecipeSqlGatewayMock, uow: UowMock) -> None:
    await new_recipe(recipe_dto, sql_gateway, uow)
    with pytest.raises(NotFoundError):
        await find_recipe_by_id("123", sql_gateway)

@pytest.mark.asyncio
async def test_get_filtered_recipes_filtered_recipes_returned(recipes: list[Recipe], sql_gateway: RecipeSqlGatewayMock) -> None:
    for recipe in recipes:
        await sql_gateway.create_recipe(recipe)
    filter = RecipeFilter(
        include=["onion", "pepper"],
        exclude=["butter"]
    )
    filtered_recipes = await get_filtered_recipes(filter, sql_gateway)
    assert filtered_recipes
    for recipe in filtered_recipes:
        assert set(recipe.ingredients).issuperset(filter.include)
        assert set(recipe.ingredients).isdisjoint(filter.exclude)