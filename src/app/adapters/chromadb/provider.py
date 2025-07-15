import chromadb
from chromadb import ClientAPI, Embeddings
from dishka import Provider, provide, Scope
from langchain_chroma import Chroma

from src.app.adapters.chromadb.gateway import ChromaRecipeGateway
from src.app.application.protocols.database import AbstractChromaRecipeGateway


class ChromaProvider(Provider):
    @provide(scope=Scope.APP)
    def get_chroma_client(self) -> ClientAPI:
        return chromadb.HttpClient(host='localhost', port=8000)

    @provide(scope=Scope.APP)
    def get_recipe_vector_store(self, client: ClientAPI, embeddings: Embeddings) -> Chroma:
        vector_store = Chroma(
            client=client,
            collection_name="recipe",
            embedding_function=embeddings,
        )
        return vector_store

    @provide(scope=Scope.APP, provides=AbstractChromaRecipeGateway)
    def get_chroma_recipe_gateway(self, vector_store: Chroma) -> ChromaRecipeGateway:
        return ChromaRecipeGateway(vector_store)