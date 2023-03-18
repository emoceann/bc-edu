import sys
import json
import pytest
from core.app import app
from tortoise import Tortoise
from httpx import AsyncClient
from core.migrate import migrate
from asgi_lifespan import LifespanManager


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    await Tortoise.init(
        db_url='sqlite://./db.sqlite',
        modules={
            "migrate": ["core.migrate"],
            "account": ["app.account.dao"],
            "telegram": ["app.telegram.dao"],
            "dictionary_utm": ["app.dictionary.utm.dao"],
            "integration_bizon365": ["app.integration.bizon365.dao"],
            "nowpayments": ["app.integration.nowpayments.dao"]
        }
    )
    # await migrate()
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
    await Tortoise.close_connections()
