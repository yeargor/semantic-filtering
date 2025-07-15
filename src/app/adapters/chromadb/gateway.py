from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.app.adapters.chromadb.mappers import from_recipe, to_recipe
from src.app.application.models.recipe import Recipe
from src.app.application.protocols.database import AbstractChromaRecipeGateway
from src.app.application.protocols.retriever import AbstractRecipeRetriever


class ChromaRecipeGateway(AbstractChromaRecipeGateway):
    def __init__(
            self,
            vector_store: Chroma,
            retriever: AbstractRecipeRetriever
    ):
        self.vector_store = vector_store
        self.retriever = retriever

    def search(self, query: str) -> List[Recipe]:
        documents_list = self.retriever.invoke(input=query)
        recipes = [to_recipe(doc) for doc in documents_list]
        return recipes

    def create_recipe(self, recipe: Recipe):
        recipe_document = from_recipe(recipe)
        langchain_document = Document(
            page_content=recipe_document.content,
            metadata=recipe_document.metadata,
            id=str(recipe_document.id),
        )
        self.vector_store.add_documents(documents=[langchain_document])
        return langchain_document.id

    def update_recipe(self, recipe_id: str, recipe: Recipe) -> None:
        recipe_document = from_recipe(recipe)
        langchain_document = Document(
            page_content=recipe_document.content,
            metadata=recipe_document.metadata
        )
        self.vector_store.update_document(document_id=str(id), document=langchain_document)

    def delete_recipe(self, recipe_id: str) -> None:
        self.vector_store.delete(document_id=str(id))