from aiogram import types
from aiogram.dispatcher import FSMContext
from app.telegram.deps import bot, dp, templates
from app.telegram.handler import NewUser


test_template = templates.get_template('question.html')


@dp.message_handler(state=NewUser.newbie)
async def newbie_state(msg: types.Message, state: FSMContext):
    if msg.text == 'изучить базу знаний':
        await NewUser.newbie_knowledge_base.set()
        markup = types.InlineKeyboardMarkup()
        for key, value in just_dict.items():
            markup.add(types.InlineKeyboardButton(text=value,
                                                  callback_data=key))
        await msg.answer('Выбери', reply_markup=markup)
    if msg.text == 'пройти тест':
        await NewUser.newbie_q1.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('начать тест')
        await msg.answer('Ну что начнем тест?', reply_markup=markup)


@dp.callback_query_handler(state=NewUser.newbie_knowledge_base)  # хендлер для новичка который не выбрал тесты
async def newbie_infobase(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data)


@dp.message_handler(state=NewUser.newbie_q1)  # хендлер новичка который выбрал тесты
async def newbie_test(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
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
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q3.set()


@dp.message_handler(state=NewUser.newbie_q3)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q4.set()


@dp.message_handler(state=NewUser.newbie_q4)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q5.set()


@dp.message_handler(state=NewUser.newbie_q5)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q6.set()


@dp.message_handler(state=NewUser.newbie_q6)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q7.set()


@dp.message_handler(state=NewUser.newbie_q7)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q8.set()


@dp.message_handler(state=NewUser.newbie_q8)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q9.set()


@dp.message_handler(state=NewUser.newbie_q9)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
    else:
        await msg.answer('продолжаем')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('правильно', 'неправильно')
    await msg.answer(test_template.render(), reply_markup=markup)
    await NewUser.newbie_q10.set()


@dp.message_handler(state=NewUser.newbie_q10)
async def newbie_q2(msg: types.Message, state: FSMContext):
    if msg.text == 'правильно':
        await msg.answer('красава')
        async with state.proxy() as data:
            data['score'] = 1
            print(data)

    await msg.answer(test_template.render())
    await state.finish()
