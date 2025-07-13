from typing import Dict, Any
from langchain_core.prompts import PromptTemplate

from src.app.application.models.chat.prompt import Prompt
from src.app.application.models.chat.state import State
from src.app.application.protocols.database import AbstractChromaRecipeGateway
from src.app.application.protocols.llm import LLM


class Nodes:
    def __init__(
            self,
            database: AbstractChromaRecipeGateway,
            llm: LLM
    ):
        self.database = database
        self.llm = llm

    def retrieve(self, state: State) -> Dict[str, Any]:
        retrieved_docs = self.database.similarity_search(state["question"])
        return {"context": retrieved_docs}

    def generate(self, state: State) -> Dict[str, Any]:
        prompt = PromptTemplate.from_template(Prompt.template)
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}