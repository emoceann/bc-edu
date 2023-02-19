from aiogram import types
import app.telegram.handler
from .services import app, bot, dp
from aiogram import Bot, Dispatcher
from fastapi.responses import HTMLResponse


@app.post("/internal")
async def webhook(update: dict):
    Bot.set_current(value=bot)
    Dispatcher.set_current(value=dp)
    await dp.process_update(update=types.Update(**update))
    return HTMLResponse(status_code=200)
