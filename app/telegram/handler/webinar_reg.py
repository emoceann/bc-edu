from app.telegram.deps import dp, bot
from app.telegram.handler.states import NewUser
from aiogram.dispatcher import FSMContext
from aiogram import types

from app.telegram.services import get_template


@dp.message_handler(state=NewUser.webinar_reg_start)
async def webinar_reg(msg: types.Message, state: FSMContext):
    text = get_template('webinar_reg.html', content_list=dict(webinar_reg={}))
    await NewUser.webinar_user_name.set()
    await msg.answer(text['webinar_reg'])


@dp.message_handler(state=NewUser.webinar_user_name)
async def webinar_user_name(msg: types.Message, state: FSMContext):
    text = get_template('webinar_reg.html', content_list=dict(webinar_reg2={}))
    async with state.proxy() as data:
        data['name'] = msg.text

    await NewUser.webinar_user_email.set()
    await msg.answer(text['webinar_reg2'])


@dp.message_handler(state=NewUser.webinar_user_email)
async def webinar_user_email(msg: types.Message, state: FSMContext):
    text = get_template('webinar_reg.html', content_list=dict(webinar_reg3={}))
    async with state.proxy() as data:
        data['email'] = msg.text

    await NewUser.webinar_user_number.set()
    await msg.answer(text['webinar_reg3'])


@dp.message_handler(state=NewUser.webinar_user_number)
async def webinar_user_number(msg: types.Message, state: FSMContext):
    text = get_template('webinar_reg.html', content_list=dict(webinar_reg4={}, button_time={}))
    async with state.proxy() as data:
        data['phone_number'] = msg.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*(i for i in text['button_time'].split('\n')))
    await NewUser.webinar_user_time.set()
    await msg.answer(text['webinar_reg4'], reply_markup=markup)


@dp.message_handler(state=NewUser.webinar_user_time)
async def webinar_reg_end(msg: types.Message, state: FSMContext):
    text = get_template('webinar_reg.html', content_list=dict(webinar_reg_end={'time': msg.text}))
    async with state.proxy() as data:
        data['webinar_time'] = msg.text

    print(await state.get_data())
    await msg.answer(text['webinar_reg_end'])
