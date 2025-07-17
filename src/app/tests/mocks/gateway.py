import uuid
from typing import List, Any

from src.app.application.common.dto.recipe.recipe import RecipeFilter
from src.app.application.models.recipe import Recipe
from src.app.application.protocols.database import AbstractSqlRecipeGateway, AbstractChromaRecipeGateway


class RecipeSqlGatewayMock(AbstractSqlRecipeGateway):
    def __init__(self) -> None:
        self.recipes: dict[str,Recipe] = {}

    async def create_recipe(self, recipe: Recipe) -> None:
        recipe.id = str(uuid.uuid4())
        self.recipes[recipe.id]=recipe

    async def find_recipe_by_id(self, recipe_id: str) -> Recipe:
        return self.recipes.get(recipe_id)

    async def find_all(self, filters: RecipeFilter):
        recipes = list(self.recipes.values())
        if filters.exclude is not None:
            exclude_lower = {i.lower() for i in filters.exclude}
            exclude_filtered = []
            for recipe in recipes:
                if set(recipe.ingredients).isdisjoint(exclude_lower):
                    exclude_filtered.append(recipe)
            recipes = exclude_filtered
        if filters.include is not None:
            include_lower = {i.lower() for i in filters.include}
            include_filtered = []
            for recipe in recipes:
                if set(recipe.ingredients).issuperset(include_lower):
                    include_filtered.append(recipe)
            recipes = include_filtered
        return recipes

    async def update_recipe(self, recipe: Recipe) -> Recipe:
        pass

    async def delete_recipe(self, recipe_id: str) -> None:
        pass

class RecipeChromaGatewayMock(AbstractChromaRecipeGateway):
    def __init__(self) -> None:
        self.recipes: list[Recipe] = []

    async def search(self, query: str) -> List[Any]:
        pass

    async def create_recipe(self, recipe: Recipe) -> None:
        self.recipes.append(recipe)

    def update_recipe(self, recipe_id: str, recipe: Recipe) -> None:
        pass

    def delete_recipe(self, recipe_id: str) -> None:
        pass