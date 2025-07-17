from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.adapters.sqlalchemy_db.exceptions import GatewayError
from src.app.application.common.dto.recipe.recipe import RecipeFilter
from src.app.application.models.recipe import Recipe
from src.app.application.protocols.database import AbstractSqlRecipeGateway

class RecipeSqlGateway(AbstractSqlRecipeGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_recipe(self, recipe: Recipe) -> None:
        self.session.add(recipe)
        try:
            await self.session.flush((recipe,))
        except IntegrityError as e:
            raise GatewayError(f"Error occurred while creating recipe: {e}") from e

    async def find_all(self, filters: RecipeFilter):
        stmt = select(Recipe)
        if filters.include:
            include = [i.lower() for i in filters.include]
            stmt = stmt.where(Recipe.ingredients.contains(include))
        if filters.exclude:
            exclude = [i.lower() for i in filters.exclude]
            stmt = stmt.where(~Recipe.ingredients.overlap(exclude))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def find_recipe_by_id(self, recipe_id: str) -> Recipe | None:
        recipe = await self.session.get(Recipe, recipe_id)
        return recipe

    async def update_recipe(self, recipe: Recipe) -> None:
        self.session.add(recipe)
        try:
            await self.session.flush((recipe,))
        except IntegrityError as e:
            raise GatewayError(f"Error occurred while updating recipe: {e}") from e

    async def delete_recipe(self, recipe_id: str) -> None:
        stmt = delete(Recipe).where(Recipe.id == recipe_id)
        await self.session.execute(stmt)