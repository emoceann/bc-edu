from aiogram import types
from aiogram.dispatcher import FSMContext
from app.telegram.deps import bot, dp, templates
from app.telegram.handler.states import NewUser
from app.telegram.services import register_user


@dp.message_handler(commands='start')
async def cmd_start(msg: types.Message, state: FSMContext):
    await register_user(utm_id=msg.get_args(), msg=msg, usr=msg.from_user)

    await NewUser.new_or_experienced.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('da', 'net')
    await msg.answer(templates.get_template('start.html').render(), reply_markup=markup)


@dp.message_handler(state=NewUser.new_or_experienced)
async def check_exp(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if msg.text == 'da':
        await NewUser.experienced.set()
    if msg.text == 'net':
        await NewUser.newbie.set()
        await msg.answer(templates.get_template('newbie.html').render(),
                         reply_markup=markup.add('пройти тест', 'изучить базу знаний'))
