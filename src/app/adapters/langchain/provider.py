from chromadb import Embeddings
from dishka import Provider, provide, Scope
from langchain_google_vertexai import ChatVertexAI
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.app.application.models.chat.state import State
from src.app.application.nodes import Nodes
from src.app.application.protocols.database import AbstractChromaRecipeGateway
from src.app.application.protocols.graph import CompiledGraph
from src.app.application.protocols.llm import LLM

class LangChainProvider(Provider):
    @provide(scope=Scope.APP)
    def get_llm(self) -> LLM:
        return ChatVertexAI(
            model="gemini-2.5-flash",
            project="elemental-kite-456917-j6",
            location="us-central1"
        )

    @provide(scope=Scope.APP)
    def get_embeddings(self) -> Embeddings:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    @provide(scope=Scope.APP)
    def get_nodes(self, gateway: AbstractChromaRecipeGateway, llm: LLM) -> Nodes:
        return Nodes(gateway, llm)

    @provide(scope=Scope.APP)
    def get_compiled_graph(self, nodes: Nodes) -> CompiledGraph:
        graph_builder = StateGraph(State)
        graph_builder.add_node("retrieve", nodes.retrieve)
        graph_builder.add_node("generate", nodes.generate)

        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "generate")
        graph_builder.add_edge("generate", END)

        compiled_graph = graph_builder.compile()
        return compiled_graph