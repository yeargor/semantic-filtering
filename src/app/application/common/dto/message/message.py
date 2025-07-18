from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    data: str = Field(title="Search Query", description="The natural language query for semantic search.")