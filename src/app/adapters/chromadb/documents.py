from dataclasses import dataclass
from typing import Any


@dataclass
class RecipeDocument:
    id: str
    content: str
    metadata: dict[str, Any]