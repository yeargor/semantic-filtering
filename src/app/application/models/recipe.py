from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Cuisine(str, Enum):
    ITALIAN="italian"
    FRENCH="french"

@dataclass
class Recipe:
    id: str = field(init=False)
    title: str
    ingredients: List[str]
    instructions: str
    cooking_time: int
    difficulty: Difficulty
    cuisine: Cuisine


