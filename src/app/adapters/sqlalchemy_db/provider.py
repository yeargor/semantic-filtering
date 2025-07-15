import os
from typing import Iterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.app.adapters.sqlalchemy_db.gateway import RecipeSqlGateway
from src.app.application.protocols.database import UoW, AbstractSqlRecipeGateway


class SqlAlchemyProvider(Provider):
    @provide(scope=Scope.APP, provides=async_sessionmaker)
    def get_async_session_maker(self) -> async_sessionmaker[AsyncSession]:
        db_uri = os.getenv("DB_URI")
        if not db_uri:
            raise ValueError("DB_URI env variable is not set")

        async_engine = create_async_engine(
            db_uri,
            echo=True,
            pool_size=15,
            max_overflow=15,
            connect_args={
                "command_timeout": 5,
            },
        )
        return async_sessionmaker(async_engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_async_session(self, async_session_maker: async_sessionmaker[AsyncSession]) -> Iterable[AsyncSession]:
         async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST, provides=UoW)
    def get_uow_session(self, session: AsyncSession) -> Iterable[AsyncSession]:
        return session

    @provide(scope=Scope.REQUEST, provides=AbstractSqlRecipeGateway)
    def get_recipe_sql_gateway(self, session: AsyncSession) -> RecipeSqlGateway:
        return RecipeSqlGateway(session)