from dataclasses import dataclass, field
from enum import Enum
from typing import List

class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Cuisine(str, Enum):
    ITALIAN="Italian"
    FRENCH="French"

@dataclass
class Recipe:
    id: str = field(init=False)
    title: str
    ingredients: List[str]
    instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: Cuisine


