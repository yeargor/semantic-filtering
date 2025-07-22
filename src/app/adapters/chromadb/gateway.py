import uuid
from typing import List
from langchain_core.embeddings import Embeddings
from chromadb.api.models.AsyncCollection import AsyncCollection

from src.app.adapters.chromadb.mappers import from_recipe, from_langchain_document, from_chroma_document
from src.app.application.models.recipe import Recipe
from src.app.application.protocols.database import AbstractChromaRecipeGateway
from src.app.application.protocols.retriever import AbstractRecipeRetriever


class ChromaRecipeGateway(AbstractChromaRecipeGateway):
    def __init__(
            self,
            collection: AsyncCollection,
            retriever: AbstractRecipeRetriever,
            embeddings: Embeddings
    ):
        self.collection = collection
        self.retriever = retriever
        self.embeddings = embeddings

    async def search(self, query: str) -> List[Recipe]:
        documents_list = await self.retriever.ainvoke(input=query)
        recipes = [from_langchain_document(doc) for doc in documents_list]
        return recipes

    async def get_by_id(self, recipe_id: str) -> Recipe | None:
        document = await self.collection.get(ids=recipe_id)
        if document['documents']:
            return from_chroma_document(document)

    async def create_recipe(self, recipe: Recipe) -> str:
        recipe_document = from_recipe(recipe)
        embeddings = self.embeddings.embed_query(recipe_document.content)
        if recipe.id is None:
            recipe.id = str(uuid.uuid4())
        await self.collection.add(
            ids=recipe.id,
            embeddings=embeddings,
            documents=recipe_document.content,
            metadatas=recipe_document.metadata
        )
        return recipe.id

    async def update_recipe(self, recipe_id: str, recipe: Recipe) -> None:
        recipe_document = from_recipe(recipe)
        embeddings = self.embeddings.embed_query(recipe_document.content)
        await self.collection.update(
            ids=recipe_id,
            embeddings=embeddings,
            documents=recipe_document.content,
            metadatas=recipe_document.metadata
        )

    async def delete_recipe(self, recipe_id: str) -> None:
        await self.collection.delete(ids=[recipe_id])