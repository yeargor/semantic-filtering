import uuid

from sqlalchemy import MetaData, Table, Column, String, Text, Integer
from sqlalchemy.orm import registry
from sqlalchemy.dialects.postgresql import UUID, ENUM, ARRAY

from src.app.application.models.recipe import Cuisine, Difficulty, Recipe


metadata_obj = MetaData()
mapper_registry = registry()

recipe = Table(
    "recipe",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(), nullable=False),
    Column("ingredients", ARRAY(String), nullable=False),
    Column("instructions", Text, nullable=False),
    Column("cooking_time", Integer, nullable=False),
    Column("difficulty", ENUM(Difficulty, name="difficulty_enum"), nullable=False),
    Column("cuisine", ENUM(Cuisine, name="cuisine_enum"), nullable=False),
)

mapper_registry.map_imperatively(Recipe, recipe)

