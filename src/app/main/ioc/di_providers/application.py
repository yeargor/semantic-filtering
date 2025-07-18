from dishka import Provider, provide, Scope

from src.app.application.broker_handler import RecipeHandler


class ApplicationProvider(Provider):
    recipe_handler = provide(
        source=RecipeHandler,
        scope=Scope.APP
    )