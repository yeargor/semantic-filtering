from abc import ABC, abstractmethod
from typing import List, Any

from src.app.application.common.dto.recipe.recipe import RecipeFilter
from src.app.application.models.recipe import Recipe


class AbstractChromaRecipeGateway(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[Any]:
        pass

    @abstractmethod
    async def create_recipe(self, recipe: Recipe) -> None:
        pass

    @abstractmethod
    async def update_recipe(self, recipe_id: str, recipe: Recipe) -> None:
        pass

    @abstractmethod
    async def delete_recipe(self, recipe_id: str) -> None:
        pass

class AbstractSqlRecipeGateway(ABC):
    @abstractmethod
    async def create_recipe(self, recipe: Recipe) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_recipe_by_id(self, recipe_id: str) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, filters: RecipeFilter) -> List[Recipe]:
        raise NotImplementedError

    @abstractmethod
    async def update_recipe(self, recipe: Recipe) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    async def delete_recipe(self, recipe_id: str) -> None:
        raise NotImplementedError

class UoW(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self):
        raise NotImplementedError