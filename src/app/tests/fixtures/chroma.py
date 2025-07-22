from typing import Any, Generator

import pytest
from chromadb import HttpClient, AsyncHttpClient
from langchain_chroma import Chroma
from testcontainers.chroma import ChromaContainer
import time

from src.app.tests.fixtures.langchain import get_embeddings


class CustomChromaContainer(ChromaContainer):
    def _healthcheck(self):
        time.sleep(2)

@pytest.fixture(scope="session")
def chroma_container() -> Generator[ChromaContainer, Any, None]:
    with CustomChromaContainer(image="chromadb/chroma:1.0.14.dev40") as chroma:
        yield chroma

@pytest.fixture(scope="session")
async def chroma_async_client(chroma_container):
    config = chroma_container.get_config()
    return await AsyncHttpClient(
        host=config["host"],
        port=config["port"]
    )

@pytest.fixture(scope="session")
async def get_async_collection(chroma_async_client,get_embeddings):
    return await chroma_async_client.get_or_create_collection(
        name="recipe"
    )

@pytest.fixture(scope="session")
def chroma_client(chroma_container):
    config = chroma_container.get_config()
    return HttpClient(
        host=config["host"],
        port=config["port"]
    )

@pytest.fixture(scope="session")
def vector_store(chroma_client,get_embeddings) -> Chroma:
    return Chroma(
        client=chroma_client,
        collection_name="recipe",
        embedding_function=get_embeddings
    )