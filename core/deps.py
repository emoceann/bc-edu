from .app import app
from .settings import settings
from tortoise.contrib.fastapi import register_tortoise, connections


@app.on_event("startup")
async def on_startup():
    register_tortoise(
        app=app,
        db_url=settings.DB_CONNECTION,
        generate_schemas=True,
        add_exception_handlers=True,
        modules={
            "telegram": ["app.telegram.dao"],
            "dictionary.utm": ["app.dictionary.utm.dao"]
        }
    )


@app.on_event("shutdown")
async def on_shutdown():
    await connections.close_all()
