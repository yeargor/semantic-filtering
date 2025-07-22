import os

import chromadb
from chromadb import ClientAPI, AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection
from dishka import Provider, provide, Scope
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

from src.app.adapters.chromadb.config import ChromaConfig
from src.app.adapters.chromadb.gateway import ChromaRecipeGateway
from src.app.application.protocols.database import AbstractChromaRecipeGateway
from src.app.application.protocols.retriever import AbstractRecipeRetriever


class ChromaProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> ChromaConfig:
        return ChromaConfig(
            os.getenv("CHROMA_HOST","localhost"),
            int(os.getenv("CHROMA_PORT",8000))
        )

    @provide(scope=Scope.APP)
    async def get_async_chroma_client(self, config: ChromaConfig) -> AsyncClientAPI:
        return await chromadb.AsyncHttpClient(
            config.host,
            config.port
        )

    @provide(scope=Scope.APP)
    async def get_recipe_async_collection(
            self,
            client: AsyncClientAPI
    ) -> AsyncCollection:
        return await client.get_or_create_collection(
            name="recipe"
        )

    @provide(scope=Scope.APP)
    def get_chroma_client(self, config: ChromaConfig) -> ClientAPI:
        return chromadb.HttpClient(
            host=config.host,
            port=config.port
        )

    @provide(scope=Scope.APP, provides=Chroma)
    def get_recipe_vector_store(
            self,
            client: ClientAPI,
            embeddings: Embeddings
    ) -> Chroma:
        return Chroma(
            client=client,
            collection_name="recipe",
            embedding_function=embeddings,
        )

    @provide(scope=Scope.APP, provides=AbstractChromaRecipeGateway)
    def get_chroma_recipe_gateway(
            self,
            collection: AsyncCollection,
            retriever: AbstractRecipeRetriever,
            embeddings: Embeddings
    ) -> ChromaRecipeGateway:
        return ChromaRecipeGateway(
            collection,
            retriever,
            embeddings,
        )