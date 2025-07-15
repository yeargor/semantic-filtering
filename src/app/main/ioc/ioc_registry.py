from typing import Iterable

from dishka import Provider

from src.app.adapters.chromadb.provider import ChromaProvider
from src.app.adapters.kafka.provider import KafkaProvider
from src.app.adapters.langchain.provider import LangChainProvider
from src.app.adapters.sqlalchemy_db.provider import SqlAlchemyProvider
from src.app.main.ioc.di_providers.application import ApplicationProvider


def get_providers() -> Iterable[Provider]:
    return (
        SqlAlchemyProvider(),
        ChromaProvider(),
        KafkaProvider(),
        LangChainProvider(),
        ApplicationProvider(),
    )