import pytest
from dotenv import load_dotenv
from google.oauth2 import service_account
from langchain.retrievers import SelfQueryRetriever
from langchain_google_vertexai import ChatVertexAI
from langchain_huggingface import HuggingFaceEmbeddings

from src.app.adapters.langchain.config import load_config
from src.app.adapters.langchain.recipe_meta import get_document_content_description, get_metadata_field_info


@pytest.fixture()
def get_llm() -> ChatVertexAI:
    load_dotenv()
    config = load_config()
    credentials = service_account.Credentials.from_service_account_file(config.credentials)
    return ChatVertexAI(
        model="gemini-2.5-flash",
        project=config.project,
        location=config.location,
        credentials=credentials,
    )

@pytest.fixture(scope="session")
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@pytest.fixture()
def get_retriever(get_llm, vector_store) -> SelfQueryRetriever:
    document_content_description = get_document_content_description()
    metadata_field_info = get_metadata_field_info()
    return SelfQueryRetriever.from_llm(
        get_llm,
        vector_store,
        document_content_description,
        metadata_field_info
    )