from fastapi import FastAPI

from src.app.api.recipe import recipe_router

def init_routers(app: FastAPI):
    app.include_router(recipe_router)