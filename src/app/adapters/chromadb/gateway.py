from typing import List, Any

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.app.adapters.chromadb.documents import RecipeDocument, to_recipe
from src.app.application.models.recipe import Recipe
from src.app.application.protocols.database import AbstractChromaRecipeGateway


class ChromaRecipeGateway(AbstractChromaRecipeGateway):
    def __init__(
            self,
            vector_store: Chroma
    ):
        self.vector_store = vector_store

    def similarity_search(self, query: str, filter: dict[str, str] | None = None) -> List[Any]:
        return self.vector_store.similarity_search(query=query, filter=filter)

    def create_recipe(self, recipe: Recipe):
        recipe_document = RecipeDocument.from_recipe(recipe)
        langchain_document = Document(
            page_content=recipe_document.content,
            metadata=recipe_document.metadata,
            id=str(recipe_document.id),
        )
        self.vector_store.add_documents(documents=[langchain_document])
        return langchain_document.id

    def update_recipe(self, recipe_id: str, recipe: Recipe) -> None:
        recipe_document = RecipeDocument.from_recipe(recipe)
        langchain_document = Document(
            page_content=recipe_document.content,
            metadata=recipe_document.metadata
        )
        self.vector_store.update_document(document_id=str(id), document=langchain_document)

    def delete_recipe(self, recipe_id: str) -> None:
        self.vector_store.delete(document_id=str(id))
