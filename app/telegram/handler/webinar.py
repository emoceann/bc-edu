from app.telegram.deps import dp, bot
from app.telegram.handler.states import NewUser
from aiogram.dispatcher import FSMContext
from aiogram import types
from app.integration.bizon365 import services as bizon_services
from app.account import services as account_services


@dp.message_handler(state=NewUser.webinar_start)
async def webinar_start(msg: types.Message):
    user_fields = await account_services.get_user_by_fields(msg.from_user.id, 'id', 'username', 'email')
    if not user_fields.username:
        user_fields.username = ''
    webinar_link = await bizon_services.create_link_webinar(
        webinar=await bizon_services.get_last_webinar_title(),
        username=user_fields.username,
        email=user_fields.email,
        tg_id=user_fields.id
    )
    await msg.answer(webinar_link)
