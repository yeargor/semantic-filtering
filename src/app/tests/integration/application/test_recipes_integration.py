import time
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
        title="First recipe",
        ingredients=["onion", "pepper"],
        instructions="Some instructions",
        cooking_time=0,
        difficulty=Difficulty.EASY,
        cuisine=Cuisine.FRENCH
    )
    second_recipe = Recipe(
        title="Second recipe",
        ingredients=["cheese", "butter"],
        instructions="Some instructions",
        cooking_time=0,
        difficulty=Difficulty.EASY,
        cuisine=Cuisine.FRENCH
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
    recipes = await gateway.search("onion in ingredients")
    assert "onion" in recipes[0].ingredients

async def test_semantic_search_recipe_recipes_filtered_correctly(
        vector_store: Chroma,
        get_retriever: SelfQueryRetriever,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(vector_store,get_retriever)
    for recipe in recipes:
        await gateway.create_recipe(recipe)
    recipes = await gateway.search("without onion in ingredients")
    assert "onion" not in recipes[0].ingredients