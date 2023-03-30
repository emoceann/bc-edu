import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from app.telegram.deps import bot, dp
from app.telegram.handler.states import NewUser
from app.telegram.services import get_template


@dp.message_handler(state=NewUser.notfiy_not_active)
async def notify(msg: types.Message, state: FSMContext):
    text = get_template('notify.html', content_list=dict(alliance_link={}))
    if msg.text == 'Присоединиться к Banana Crypto Alliance':
        await msg.reply(text['alliance_link'])

    if msg.text.startswith('Зарегистрироваться на вебинар'):
        text = get_template('webinar_reg.html', content_list=dict(webinar_info={}, button_1={}))
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True).add(text['button_1'])
        await msg.answer(text['webinar_info'], reply_markup=markup)
        await NewUser.webinar_reg_start.set()

    if msg.text == 'Посмотреть результаты Banana Crypto Alliance📊':
        text = get_template('newbie_knowledge_base.html', content_list=dict(stats={}, buttons5={}))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            *(i for i in text['buttons5'].split('\n')))
        await msg.reply(text['stats'], reply_markup=markup)
        await NewUser.webinar_reg_start.set()

    if msg.text == 'Пройти испытание и заработать Banana-coins':
        await NewUser.newbie_q1.set()
        text = get_template('questions.html', content_list=dict(start_test={}))
        await msg.answer(text['start_test'])
        await asyncio.sleep(5)
        text = get_template('questions.html', content_list=dict(question_1={}, keyboard_3={}))
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(*(i for i in text['keyboard_3'].split()))
        await msg.answer(text['question_1'], reply_markup=markup)
