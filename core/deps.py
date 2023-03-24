from .app import app
from .settings import settings
from .logger import *
from .migrate import migrate
from tortoise import Tortoise


@app.on_event("startup")
async def on_startup():
    await Tortoise.init(
        db_url=settings.DB_CONNECTION,
        modules={
            "migrate": ["core.migrate"],
            "account": ["app.account.dao"],
            "dictionary_utm": ["app.dictionary.utm.dao"],
            "integration_bizon365": ["app.integration.bizon365.dao"],
            "nowpayments": ["app.integration.nowpayments.dao"],
            "telegram": ["app.telegram.dao"],
            "notion": ["core.contrib.notion.dao"]
        }
    )
    await migrate()


@app.on_event("shutdown")
async def on_shutdown():
    await Tortoise.close_connections()
