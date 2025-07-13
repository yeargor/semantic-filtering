from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from src.app.application.models.recipe import Difficulty, Cuisine


class RecipeDto(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: Cuisine

class RecipeUpdateDto(BaseModel):
    title: str | None = None
    ingredients: List[str] | None = None
    instructions: str | None = None
    cooking_time: int | None = None
    difficulty: Difficulty | None = None
    cuisine: Cuisine | None = None

@dataclass
class RecipeResponse:
    title: str
    ingredients: List[str]
    instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: Cuisine

@dataclass
class RecipeCreateResponse:
    id: str