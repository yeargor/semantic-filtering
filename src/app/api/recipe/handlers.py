from fastapi import Request, FastAPI
from starlette.responses import JSONResponse

from src.app.adapters.kafka.exceptions import KafkaConsumerError
from src.app.adapters.sqlalchemy_db.exceptions import GatewayError
from src.app.application.common.exceptions import NotFoundError

async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def gateway_error_handler(request: Request, exc: GatewayError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})

async def kafka_error_handler(request: Request, exc: KafkaConsumerError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})