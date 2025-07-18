import pytest
from sqlalchemy import sql,select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.adapters.sqlalchemy_db.gateway import RecipeSqlGateway
from src.app.application.common.dto.recipe.recipe import RecipeFilter
from src.app.application.models.recipe import Recipe, Cuisine, Difficulty


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
def recipe() -> Recipe:
    return Recipe(
        title="First recipe",
        ingredients=["onion", "pepper"],
        instructions="Some instructions",
        cooking_time=0,
        difficulty=Difficulty.EASY,
        cuisine=Cuisine.FRENCH
    )

async def test_db(session: AsyncSession):
    result = await session.execute(select(sql.true()))
    assert result.scalar() is True

async def test_gateway_create_find_recipe_recipe_found(session: AsyncSession):
    recipe = Recipe(
        title="First recipe",
        ingredients=["onion", "pepper"],
        instructions="Some instructions",
        cooking_time=0,
        difficulty=Difficulty.EASY,
        cuisine=Cuisine.FRENCH
    )
    gateway = RecipeSqlGateway(session)
    await gateway.create_recipe(recipe)
    await session.commit()

    founded_recipe = await gateway.find_recipe_by_id(recipe.id)
    assert founded_recipe

async def test_get_filtered_recipes_filtered_recipes_returned(recipes: list[Recipe], session: AsyncSession):
    gateway = RecipeSqlGateway(session)
    filter = RecipeFilter(
        include=["onion", "pepper"],
        exclude=["butter"]
    )
    for recipe in recipes:
        await gateway.create_recipe(recipe)

    filtered_recipes = await gateway.find_all(filter)
    assert filtered_recipes
    for recipe in filtered_recipes:
        assert set(recipe.ingredients).issuperset(filter.include)
        assert set(recipe.ingredients).isdisjoint(filter.exclude)