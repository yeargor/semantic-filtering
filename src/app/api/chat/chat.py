from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.app.application.common.dto.message.message import MessageDTO, MessageResultDTO
from src.app.application.graph import invoke_graph
from src.app.application.models.chat.message import Message
from src.app.application.protocols.graph import CompiledGraph

chat_router = APIRouter()

@chat_router.post('/chat')
@inject
def process_chat(
        message: MessageDTO,
        compiled_graph: FromDishka[CompiledGraph],
) -> MessageResultDTO:
    graph_response = invoke_graph(compiled_graph, Message(message.data))
    return MessageResultDTO(data = graph_response.get("answer"))