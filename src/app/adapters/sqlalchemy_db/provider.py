import os
from typing import Iterable

from dishka import Provider, provide, Scope
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.app.adapters.sqlalchemy_db.gateway import RecipeSqlGateway
from src.app.application.protocols.database import UoW, AbstractSqlRecipeGateway


class SqlAlchemyProvider(Provider):
    @provide(scope=Scope.APP, provides=sessionmaker)
    def get_session_maker(self) -> sessionmaker[Session]:
        db_uri = os.getenv("DB_URI")
        if not db_uri:
            raise ValueError("DB_URI env variable is not set")

        engine = create_engine(
            db_uri,
            echo=True,
            pool_size=15,
            max_overflow=15,
            connect_args={
                "connect_timeout": 5,
            },
        )
        return sessionmaker(engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=Session)
    def get_session(self, session_maker: sessionmaker[Session]) -> Iterable[Session]:
         with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST, provides=UoW)
    def get_uow_session(self, session: Session) -> Iterable[Session]:
        return session

    @provide(scope=Scope.REQUEST, provides=AbstractSqlRecipeGateway)
    def get_recipe_sql_gateway(self, session: Session) -> RecipeSqlGateway:
        return RecipeSqlGateway(session)

# def create_session_maker() -> sessionmaker[Session]:
#     db_uri = os.getenv("DB_URI")
#     if not db_uri:
#         raise ValueError("DB_URI env variable is not set")
#
#     engine = create_engine(
#         db_uri,
#         echo=True,
#         pool_size=15,
#         max_overflow=15,
#         connect_args={
#             "connect_timeout": 5,
#         },
#     )
#     return sessionmaker(engine, autoflush=False, expire_on_commit=False)
#
# def new_session(session_maker: sessionmaker[Session]) -> Iterable[Session]:
#     with session_maker() as session:
#         yield session
#
# def new_uow(session: Session) -> Iterable[Session]:
#     return session