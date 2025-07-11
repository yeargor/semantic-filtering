from fastapi import FastAPI

from src.app.api.chat import chat_router


def init_routers(app: FastAPI):
    app.include_router(chat_router)