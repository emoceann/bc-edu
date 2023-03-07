from app.telegram.deps import dp
from app.telegram.handler.states import NewUser
from app.telegram.services import get_template
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(state=NewUser.newbie_knowledge_base)  # хендлер для новичка который не выбрал тесты
async def newbie_infobase(msg: types.Message, state: FSMContext):
    text = get_template('newbie_knowledge_base.html', content_list=dict(text_knowledge={}, buttons={}))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(*(i for i in text['buttons'].split()))
    await msg.answer(text['text_knowledge'], reply_markup=markup)

