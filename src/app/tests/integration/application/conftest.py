import pytest

from src.app.application.broker_handler import RecipeHandler
from src.app.tests.mocks.gateway import RecipeChromaGatewayMock


@pytest.fixture()
def chroma_gateway_mock() -> RecipeChromaGatewayMock:
    return RecipeChromaGatewayMock()

@pytest.fixture()
async def recipe_handler(chroma_gateway_mock: RecipeChromaGatewayMock):
    return RecipeHandler(gateway=chroma_gateway_mock)