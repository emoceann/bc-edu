from aiogram.types import *
from app.telegram.deps import bot, dp
from aiogram.dispatcher import FSMContext


@dp.message_handler()
async def start_cmd(msg: Message, state: FSMContext):
    await msg.answer(text="Hello world!")
    data = await state.get_data()
    print(data)
