from app.telegram.deps import dp, bot
from app.telegram.handler.states import NewUser
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.telegram.services import get_template


@dp.message_handler(state=NewUser.experienced_info)
async def experienced_first(msg: types.Message, state: FSMContext):
    text = get_template('expirienced.html', content_list=dict(text_exp2={}, button2={}))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['button2'].split('\n')))
    await NewUser.experienced_choose.set()
    await msg.answer(text['text_exp2'], reply_markup=markup)


@dp.message_handler(state=NewUser.experienced_choose)
async def experienced_choose(msg: types.Message, state: FSMContext):
    text = get_template(
        'expirienced.html',
        content_list=dict(stats={}, alliance_inside={}, alliance_link={}, button3={})
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['button3'].split('\n')))
    await NewUser.alliance_enter_or_webinar.set()
    if msg.text == 'Посмотреть статистику':
        await msg.answer(text['stats'], reply_markup=markup)
    if msg.text == 'Взглянуть на Alliance изнутри':
        await msg.answer(text['alliance_inside'], reply_markup=markup)
    if msg.text == 'Вступить в Alliance':
        await msg.answer(text['alliance_link'])


@dp.message_handler(state=NewUser.alliance_enter_or_webinar)
async def webreg_start(msg: types.Message, state: FSMContext):
    text = get_template('webinar_reg.html', content_list=dict(webinar_info={}, alliance_link={}, button_1={}))
    if msg.text == 'Хочу узнать больше':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(text['button_1'])
        await NewUser.webinar_reg_start.set()
        await msg.answer(text['webinar_info'], reply_markup=markup)
    if msg.text == 'Вступить в Alliance':
        await msg.answer(text['alliance_link'])
