from fastapi import FastAPI

from src.app.api.chat import chat_router
from src.app.api.recipe.recipe import recipe_router


def init_routers(app: FastAPI):
    app.include_router(chat_router)
    app.include_router(recipe_router)