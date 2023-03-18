from fastapi import APIRouter, templating
from core.settings import settings
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram import Bot, Dispatcher, types

app = APIRouter(tags=["Telegram"])
bot: Bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode='html')
storage: JSONStorage = JSONStorage(path=settings.TELEGRAM_BOT_STATE_PATH)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)
templates = templating.Jinja2Templates(directory='template/telegram')


@app.on_event("startup")
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=settings.TELEGRAM_WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await dp.storage.wait_closed()
