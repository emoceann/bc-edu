from .dao import State
from fastapi import APIRouter
from core.settings import settings
from aiogram import Bot, Dispatcher, types

app = APIRouter(tags=["Telegram"])

bot: Bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot=bot, storage=State())


@app.on_event("startup")
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=settings.TELEGRAM_WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    ...


@app.post("/internal")
async def webhook(update: dict):
    Bot.set_current(value=bot)
    Dispatcher.set_current(value=dp)
    await dp.process_update(update=types.Update(**update))
