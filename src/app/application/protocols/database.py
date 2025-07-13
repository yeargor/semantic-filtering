from abc import ABC, abstractmethod
from typing import List, Any

from src.app.application.models.recipe import Recipe

class AbstractChromaRecipeGateway(ABC):
    @abstractmethod
    def similarity_search(self, query: str, filter: dict[str, str]) -> List[Any]:
        pass

    # @abstractmethod
    # def get_recipe_by_id(self, recipe_id: str) -> Recipe:
    #     pass
    #
    # @abstractmethod
    # def create_recipe(self, recipe: Recipe) -> str:
    #     pass
    #
    # @abstractmethod
    # def update_recipe(self, id, recipe: Recipe) -> Recipe:
    #     pass
    #
    # @abstractmethod
    # def delete_recipe(self, id) -> None:
    #     pass

class AbstractSqlRecipeGateway(ABC):
    @abstractmethod
    def create_recipe(self, recipe: Recipe) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_recipe_by_id(self, recipe_id: str) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def update_recipe(self, recipe: Recipe) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def delete_recipe(self, recipe_id: str) -> None:
        raise NotImplementedError

class UoW(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def flush(self):
        raise NotImplementedError