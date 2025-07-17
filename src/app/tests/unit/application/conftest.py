import pytest

from src.app.tests.mocks.gateway import RecipeSqlGatewayMock
from src.app.tests.mocks.uow import UowMock


@pytest.fixture()
def sql_gateway() -> RecipeSqlGatewayMock:
    return RecipeSqlGatewayMock()

@pytest.fixture()
def uow() -> UowMock:
    return UowMock()