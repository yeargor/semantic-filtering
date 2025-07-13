from dotenv import load_dotenv
from fastapi import FastAPI

from src.app.api.recipe.handlers import init_handlers
from src.app.main.di import init_dependencies
from src.app.main.routers import init_routers

load_dotenv()
app = FastAPI()
init_routers(app)
init_handlers(app)
init_dependencies(app)