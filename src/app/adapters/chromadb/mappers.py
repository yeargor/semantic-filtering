import json
import uuid
from dataclasses import asdict
from enum import Enum

from langchain_core.documents import Document

from src.app.adapters.chromadb.documents import RecipeDocument
from src.app.application.models.recipe import Recipe, Difficulty, Cuisine


def from_recipe(recipe: Recipe):
    recipe_dict = asdict(recipe)
    processed_fields = {}
    content_parts = {}

    for k, v in recipe_dict.items():
        if k == "id":
            continue
        content_parts[k] = v
        if k not in ["title", "instructions"]:
            if k == "ingredients":
                processed_fields["ingredients"] = ", ".join(v)
            elif isinstance(v, Enum):
                processed_fields[k] = v.value
            else:
                processed_fields[k] = v
    return RecipeDocument(
        id=uuid.uuid4(),
        content=json.dumps(content_parts),
        metadata=processed_fields
    )

def to_recipe(document: Document) -> Recipe:
    content_data = json.loads(document.page_content)

    return Recipe(
        title=content_data["title"],
        ingredients=content_data["ingredients"],
        instructions=content_data["instructions"],
        cooking_time=content_data["cooking_time"],
        difficulty=Difficulty(content_data["difficulty"]),
        cuisine=Cuisine(content_data["cuisine"])
    )