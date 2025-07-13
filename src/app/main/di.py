import os
from functools import partial
from typing import Iterable

import chromadb
from chromadb import ClientAPI
from fastapi import Depends, FastAPI
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_google_vertexai import ChatVertexAI
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.app.adapters.chromadb.gateway import ChromaRecipeGateway
from src.app.adapters.sqlalchemy_db.gateway import RecipeSqlGateway
from src.app.adapters.sqlalchemy_db.models import metadata_obj
from src.app.application.models.chat.state import State
from src.app.application.nodes import Nodes
from src.app.application.protocols.database import AbstractChromaRecipeGateway, UoW, AbstractSqlRecipeGateway
from src.app.application.protocols.graph import CompiledGraph
from src.app.application.protocols.llm import LLM


def all_depends(cls: type) -> None:
    """
    Adds `Depends()` to the class `__init__` methods, so it can be used
    a fastapi dependency having own dependencies
    """
    init = cls.__init__
    total_ars = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(total_ars)
    )

def create_llm():
    return ChatVertexAI(
        model="gemini-2.5-flash",
        project="elemental-kite-456917-j6",
        location="us-central1"
    )

def create_client():
    return chromadb.HttpClient(host='localhost', port=8000)

def create_recipe_vector_store(client: ClientAPI, embeddings: Embeddings):
    vector_store = Chroma(
        client=client,
        collection_name="recipe",
        embedding_function=embeddings,
    )
    return vector_store

def create_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def compile_graph(nodes: Nodes):
    graph_builder = StateGraph(State)
    graph_builder.add_node("retrieve", nodes.retrieve)
    graph_builder.add_node("generate", nodes.generate)

    graph_builder.add_edge(START, "retrieve")
    graph_builder.add_edge("retrieve", "generate")
    graph_builder.add_edge("generate", END)

    compiled_graph = graph_builder.compile()
    return compiled_graph

def new_recipe_vector_gateway(vector_store: VectorStore):
    return ChromaRecipeGateway(vector_store)

def create_nodes(gateway: ChromaRecipeGateway, llm: LLM):
    return Nodes(gateway, llm)

def new_recipe_sql_gateway(session: Session = Depends(Session)):
    yield RecipeSqlGateway(session)

def new_uow(session: Session = Depends(Session)):
    return session

def create_session_maker():
    db_uri = os.getenv("DB_URI")
    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return sessionmaker(engine, autoflush=False, expire_on_commit=False)

def new_session(session_maker: sessionmaker) -> Iterable[Session]:
    with session_maker() as session:
        yield session

def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()

    embeddings_model = create_embeddings()
    llm_client = create_llm()
    vector_client = create_client()
    recipe_vector_store = create_recipe_vector_store(vector_client, embeddings_model)
    recipe_vector_gateway = new_recipe_vector_gateway(recipe_vector_store)
    nodes = create_nodes(recipe_vector_gateway, llm_client)
    compiled_graph = compile_graph(nodes)

    app.dependency_overrides[Session] = partial(new_session, session_maker)
    app.dependency_overrides[UoW] = new_uow
    app.dependency_overrides[AbstractSqlRecipeGateway] = new_recipe_sql_gateway

    app.dependency_overrides[AbstractChromaRecipeGateway] = lambda: recipe_vector_gateway
    app.dependency_overrides[ClientAPI] = lambda: vector_client
    app.dependency_overrides[Embeddings] = lambda: embeddings_model
    app.dependency_overrides[LLM] = lambda: llm_client
    app.dependency_overrides[CompiledGraph] = lambda: compiled_graph
    app.dependency_overrides[Nodes] = lambda: nodes

    all_depends(Nodes)
