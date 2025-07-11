from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.api.dto.message import MessageDTO, MessageResultDTO
from src.app.application.graph import invoke_graph
from src.app.application.models.message import Message
from src.app.application.protocols.graph import CompiledGraph

chat_router = APIRouter()

@chat_router.post('/chat')
def process_chat(
        message: MessageDTO,
        compiled_graph: Annotated[CompiledGraph, Depends()],
) -> MessageResultDTO:
    graph_response = invoke_graph(compiled_graph, Message(message.data))
    return MessageResultDTO(data = graph_response.get("answer"))