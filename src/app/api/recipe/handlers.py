from fastapi import Request, FastAPI
from starlette.responses import JSONResponse

from src.app.adapters.sqlalchemy_db.exceptions import GatewayError
from src.app.application.common.exceptions import NotFoundError

def init_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(GatewayError, gateway_error_handler)

async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def gateway_error_handler(request: Request, exc: GatewayError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})