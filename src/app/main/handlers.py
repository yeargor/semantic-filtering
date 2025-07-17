from fastapi import FastAPI

from src.app.adapters.kafka.exceptions import KafkaConsumerError
from src.app.adapters.sqlalchemy_db.exceptions import GatewayError
from src.app.api.handlers import not_found_error_handler, gateway_error_handler, kafka_error_handler
from src.app.application.common.exceptions import NotFoundError


def init_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(GatewayError, gateway_error_handler)
    app.add_exception_handler(KafkaConsumerError, kafka_error_handler)