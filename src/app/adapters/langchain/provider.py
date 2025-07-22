from dishka import Provider, provide, Scope
from langchain_chroma import Chroma
from langchain_google_vertexai import ChatVertexAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.embeddings import Embeddings

from src.app.adapters.langchain.config import load_config
from src.app.adapters.langchain.recipe_meta import get_document_content_description, \
    get_metadata_field_info
from src.app.application.protocols.llm import LLM
from src.app.application.protocols.retriever import AbstractRecipeRetriever


class LangChainProvider(Provider):
    @provide(scope=Scope.APP, provides=LLM)
    def get_llm(self) -> ChatVertexAI:
        config = load_config()
        return ChatVertexAI(
            model="gemini-2.5-flash",
            project=config.project,
            location=config.location,
        )

    @provide(scope=Scope.APP, provides=AbstractRecipeRetriever)
    def get_retriever(
            self,
            llm: LLM,
            vector_store: Chroma,
    ) -> SelfQueryRetriever:
        document_content_description = get_document_content_description()
        metadata_field_info = get_metadata_field_info()
        return SelfQueryRetriever.from_llm(
            llm,
            vector_store,
            document_content_description,
            metadata_field_info
        )

    @provide(scope=Scope.APP, provides=Embeddings)
    def get_embeddings(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")