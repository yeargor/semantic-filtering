import asyncio
import uuid

import pytest
from langchain.retrievers import SelfQueryRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.api.models.AsyncCollection import AsyncCollection

from src.app.adapters.chromadb.gateway import ChromaRecipeGateway
from src.app.application.models.recipe import Difficulty, Cuisine, Recipe

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
        get_async_collection: AsyncCollection,
        get_retriever: SelfQueryRetriever,
        get_embeddings: HuggingFaceEmbeddings,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(
        get_async_collection,
        get_retriever,
        get_embeddings
    )
    for recipe in recipes:
        await gateway.create_recipe(recipe)
    await asyncio.sleep(3)
    recipes = await gateway.search("hard italian recipe with pepperoni")
    assert "pepperoni" in recipes[0].ingredients
    assert recipes[0].difficulty == Difficulty.HARD

async def test_semantic_search_recipe_recipes_filtered_correctly(
        get_async_collection: AsyncCollection,
        get_retriever: SelfQueryRetriever,
        get_embeddings: HuggingFaceEmbeddings,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(
        get_async_collection,
        get_retriever,
        get_embeddings
    )
    for recipe in recipes:
        await gateway.create_recipe(recipe)
    recipes = await gateway.search("simple italian recipe with cheese")
    assert "pepperoni" not in recipes[0].ingredients

async def test_update_recipe_recipe_updated(
        get_async_collection: AsyncCollection,
        get_retriever: SelfQueryRetriever,
        get_embeddings: HuggingFaceEmbeddings,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(
        get_async_collection,
        get_retriever,
        get_embeddings
    )
    await gateway.create_recipe(recipes[0])
    recipe_to_update = Recipe(
        title="Updated recipe",
        ingredients=["pasta", "pepperoni"],
        instructions="It's quite fast",
        cooking_time=0,
        difficulty=Difficulty.HARD,
        cuisine=Cuisine.ITALIAN
    )
    recipe_to_update.id = recipes[0].id
    await gateway.update_recipe(recipes[0].id, recipe_to_update)
    updated_recipe = await gateway.get_by_id(recipes[0].id)
    assert updated_recipe.title == "Updated recipe"

async def test_delete_recipe_recipe_deleted(
        get_async_collection: AsyncCollection,
        get_retriever: SelfQueryRetriever,
        get_embeddings: HuggingFaceEmbeddings,
        recipes: list[Recipe]
):
    gateway = ChromaRecipeGateway(
        get_async_collection,
        get_retriever,
        get_embeddings
    )
    await gateway.create_recipe(recipes[0])
    await gateway.delete_recipe(recipes[0].id)
    assert await gateway.get_by_id(recipes[0].id) is None