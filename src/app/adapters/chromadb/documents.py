from dataclasses import dataclass
from typing import Any
from uuid import UUID

@dataclass
class RecipeDocument:
    id: UUID
    content: str
    metadata: dict[str, Any]