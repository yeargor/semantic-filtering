import asyncio
import uuid

import pytest
from langchain.retrievers import SelfQueryRetriever
from langchain_chroma import Chroma

from src.app.adapters.chromadb.gateway import ChromaRecipeGateway
from src.app.application.models.recipe import Difficulty, Cuisine, Recipe
from src.app.tests.fixtures.chroma import vector_store

@pytest.fixture
def recipes() -> list[Recipe]:
    first_recipe = Recipe(
        title="Italian recipe",
        ingredients=["pasta", "pepperoni"],
        instructions="It's quite fast",
        cooking_time=0,
        difficulty=Difficulty.HARD,
        cuisine=Cuisine.ITALIAN
    )
    second_recipe = Recipe(
        title="simple italian recipe",
        ingredients=["cheese", "butter"],
        instructions="Some instructions",
        cooking_time=0,
        difficulty=Difficulty.EASY,
        cuisine=Cuisine.ITALIAN
    )
    first_recipe.id = str(uuid.uuid4())
    second_recipe.id = str(uuid.uuid4())
    return [first_recipe, second_recipe]

async def test_semantic_search_recipe_recipes_found(
        vector_store: Chroma,
        get_retriever: SelfQueryRetriever,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(vector_store,get_retriever)
    for recipe in recipes:
        await gateway.create_recipe(recipe)
    await asyncio.sleep(3)
    recipes = await gateway.search("hard italian recipe with pepperoni")
    assert "pepperoni" in recipes[0].ingredients
    assert recipes[0].difficulty == Difficulty.HARD

async def test_semantic_search_recipe_recipes_filtered_correctly(
        vector_store: Chroma,
        get_retriever: SelfQueryRetriever,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(vector_store,get_retriever)
    for recipe in recipes:
        await gateway.create_recipe(recipe)
    recipes = await gateway.search("simple italian recipe with cheese")
    assert "pepperoni" not in recipes[0].ingredients
