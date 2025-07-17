from src.app.application.protocols.database import UoW


class UowMock(UoW):
    async def commit(self):
        pass

    async def flush(self):
        pass