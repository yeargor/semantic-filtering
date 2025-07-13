import uuid
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any
from uuid import UUID

from src.app.application.models.recipe import Recipe


@dataclass
class RecipeDocument:
    id: UUID
    content: str
    metadata: dict[str, Any]

    @staticmethod
    def from_recipe(recipe: Recipe):
        recipe_dict = asdict(recipe)
        processed_fields = {}
        for k, v in recipe_dict.items():
            if k not in ["title", "instructions"]:
                if k == "ingredients":
                    processed_fields["ingredients"] = ", ".join(v)
                elif isinstance(v, Enum):
                    processed_fields[k] = v.value
                else:
                    processed_fields[k] = v

        return RecipeDocument(
            id=uuid.uuid4(),
            content=repr(recipe),
            metadata=processed_fields
        )

