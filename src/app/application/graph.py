from typing import Dict

from src.app.application.models.message import Message
from src.app.application.protocols.graph import CompiledGraph

def invoke_graph(
        compiled_graph: CompiledGraph,
        message: Message,
) -> Dict[str, str]:
    return compiled_graph.invoke({"question": message.data})
