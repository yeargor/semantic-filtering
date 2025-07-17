from contextlib import asynccontextmanager
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI
from src.app.adapters.sqlalchemy_db.models import metadata_obj
from src.app.application.protocols.consumer import AbstractConsumer
from src.app.main.handlers import init_handlers
from src.app.main.ioc.ioc_registry import get_providers
from src.app.main.routers import init_routers

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    recipe_consumer = await container.get(AbstractConsumer)
    await recipe_consumer.start()
    yield
    await recipe_consumer.stop()
    await app.state.dishka_contaner.close()

app = FastAPI(
    title="Semantic search with CRUD support",
    lifespan=lifespan)
container = make_async_container(*get_providers())
setup_dishka(container=container, app=app)
init_routers(app)
init_handlers(app)