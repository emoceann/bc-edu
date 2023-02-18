from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from app.telegram.deps import bot, dp, templates
from aiogram.dispatcher import FSMContext


class NewUser(StatesGroup):
    new_or_experienced = State()  # стейт новичок или продвинутый
    experienced = State()  # стейт продвинутого
    newbie = State()  # стейт новичка
    newbie_base = State()
    newbie_q1 = State()
    newbie_q2 = State()
    newbie_q3 = State()
    newbie_q4 = State()
    newbie_q5 = State()
    newbie_q6 = State()
    newbie_q7 = State()
    newbie_q8 = State()
    newbie_q9 = State()
    newbie_q10 = State()


just_dict = {'1': '1', '2': '2', '3': '4', '4': '4'}


@dp.message_handler(commands='start')
async def cmd_start(msg: types.Message, state: FSMContext):
    link = msg.text.split(' ')
    print(link)
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


@dp.message_handler(state=NewUser.newbie)
async def newbie_state(msg: types.Message, state: FSMContext):
    if msg.text == 'изучить базу знаний':
        await NewUser.newbie_base.set()
        markup = types.InlineKeyboardMarkup()
        for key, value in just_dict.items():
            markup.add(types.InlineKeyboardButton(text=value,
                                                  callback_data=key))
        await msg.answer('Выбери', reply_markup=markup)
    if msg.text == 'пройти тест':
        await NewUser.newbie_q1.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('начать тест')
        await msg.answer('Ну что начнем тест?', reply_markup=markup)


@dp.callback_query_handler(state=NewUser.newbie_base)  # хендлер для новичка который не выбрал тесты
async def newbie_infobase(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data)


@dp.message_handler(state=NewUser.newbie_q1)  # хендлер новичка который выбрал тесты
async def newbie_test(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(templates.get_template('questions.html').render(), reply_markup=markup)
    await NewUser.newbie_q2.set()


@dp.message_handler(state=NewUser.newbie_q2)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')
        async with state.proxy() as data:
            data['score'] = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(templates.get_template('questions.html').render(), reply_markup=markup)
    await NewUser.newbie_q3.set()
