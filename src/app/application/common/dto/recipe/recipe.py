from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, Field

from src.app.application.common.enums import OperationType
from src.app.application.models.recipe import Difficulty, Cuisine, Recipe

class RecipeDto(BaseModel):
    title: str = Field(title="Recipe Title", description="The name of the recipe.")
    ingredients: List[str] = Field(title="Ingredients List", description="A list of ingredients required for the recipe.")
    instructions: str = Field(title="Cooking Instructions", description="Step-by-step instructions on how to prepare the recipe.")
    cooking_time: int = Field(title="Cooking Time (minutes)", description="The estimated time in minutes required to cook the recipe.")
    difficulty: Difficulty = Field(title="Difficulty Level", description="The perceived difficulty of the recipe (Easy, Medium, Hard).")
    cuisine: Cuisine = Field(title="Cuisine Type", description="The type of cuisine the recipe belongs to (Italian, French).")

class RecipeUpdateDto(BaseModel):
    title: str | None = Field(None, title="Recipe Title", description="The updated name of the recipe.")
    ingredients: List[str] | None = Field(None, title="Ingredients List", description="An updated list of ingredients for the recipe.")
    instructions: str | None = Field(None, title="Cooking Instructions", description="Updated step-by-step instructions for the recipe.")
    cooking_time: int | None = Field(None, title="Cooking Time (minutes)", description="The updated estimated time in minutes required to cook the recipe.")
    difficulty: Difficulty | None = Field(None, title="Difficulty Level", description="The updated perceived difficulty of the recipe (Easy, Medium, Hard).")
    cuisine: Cuisine | None = Field(None, title="Cuisine Type", description="The updated type of cuisine the recipe belongs to (Italian, French).")

class RecipeFilter(BaseModel):
    include: List[str] = Field([], title="Include Ingredients", description="A list of ingredients to include in the recipe search.")
    exclude: List[str] = Field([], title="Exclude Ingredients", description="A list of ingredients to exclude from the recipe search.")

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

@dataclass
class RecipeEvent:
    id: str
    operation_type: OperationType
    body: Recipe | None = None
