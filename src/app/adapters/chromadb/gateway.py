from typing import List, Any

from langchain_core.vectorstores import VectorStore

from src.app.application.protocols.database import DatabaseGateway


class ChromaGateway(DatabaseGateway):
        def __init__(self, vector_store: VectorStore):
                self.vector_store = vector_store

        def similarity_search(self, query: str) -> List[Any]:
                return self.vector_store.similarity_search(query)