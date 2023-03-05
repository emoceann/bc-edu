from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio
from app.telegram.deps import bot, dp
from app.telegram.handler.states import NewUser
from app.telegram.services import get_template


@dp.message_handler(state=NewUser.newbie_q1)  # хендлер новичка, который выбрал тесты
async def newbie_q2(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_1={}, wrong_answer_1={}, question_2={}, keyboard_3={}))
    async with state.proxy() as data:
        if msg.text == '3':
            data['banana_coins'] = 100
            await msg.answer(text['answer_1'])
        else:
            data['banana_coins'] = 0
            await msg.answer(text['wrong_answer_1'])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_3'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_2'], reply_markup=markup)
    await NewUser.newbie_q3.set()


@dp.message_handler(state=NewUser.newbie_q3)
async def newbie_q4(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_2={}, wrong_answer_2={}, question_3={}, keyboard_4={}))
    if msg.text == '1':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_2'])
    else:
        await msg.answer(text['wrong_answer_2'])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_4'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_3'], reply_markup=markup)
    await NewUser.newbie_q4.set()


@dp.message_handler(state=NewUser.newbie_q4)
async def newbie_q4(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_3={}, wrong_answer_3={}, question_4={}, keyboard_3={}))
    if msg.text == '4':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_3'])
    else:
        await msg.answer(text['wrong_answer_3'])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_3'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_4'], reply_markup=markup)
    await NewUser.newbie_q5.set()


@dp.message_handler(state=NewUser.newbie_q5)
async def newbie_q5(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_4={}, wrong_answer_4={}, question_5={}, keyboard_4={}))
    if msg.text == '2':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_4'])
    else:
        await msg.answer(text['wrong_answer_4'])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_4'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_5'], reply_markup=markup)
    await NewUser.newbie_q6.set()


@dp.message_handler(state=NewUser.newbie_q6)
async def newbie_q5(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_5={}, wrong_answer_5={}, question_6={}, keyboard_4={}))
    if msg.text == '1':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_5'])
    else:
        await msg.answer(text['wrong_answer_5'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_4'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_6'], reply_markup=markup)
    await NewUser.newbie_q7.set()


@dp.message_handler(state=NewUser.newbie_q7)
async def newbie_q6(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_6={}, wrong_answer_6={}, question_7={}, keyboard_4={}))
    if msg.text == '3':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_6'])
    else:
        await msg.answer(text['wrong_answer_6'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_4'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_7'], reply_markup=markup)
    await NewUser.newbie_q8.set()


@dp.message_handler(state=NewUser.newbie_q8)
async def newbie_q7(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_7={}, wrong_answer_7={}, question_8={}, keyboard_4={}))
    if msg.text == '1':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_7'])
    else:
        await msg.answer(text['wrong_answer_7'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_4'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_8'], reply_markup=markup)
    await NewUser.newbie_q9.set()


@dp.message_handler(state=NewUser.newbie_q9)
async def newbie_q8(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_8={}, wrong_answer_8={}, question_9={}, keyboard_3={}))
    if msg.text == '2':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_8'])
    else:
        await msg.answer(text['wrong_answer_8'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        *(i for i in text['keyboard_3'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_9'], reply_markup=markup)
    await NewUser.newbie_q10.set()


@dp.message_handler(state=NewUser.newbie_q10)
async def newbie_q10(msg: types.Message, state: FSMContext):
    text = get_template('questions.html',
                        content_list=dict(answer_9={}, wrong_answer_9={}, question_10={}, keyboard_4={}))
    if msg.text == '1':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            await msg.answer(text['answer_9'])
    else:
        await msg.answer(text['wrong_answer_9'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
        .add(*(i for i in text['keyboard_4'].split()))
    await asyncio.sleep(3)
    await msg.answer(text['question_10'], reply_markup=markup)
    await NewUser.newbie_test_result.set()


@dp.message_handler(state=NewUser.newbie_test_result)
async def newbie_result(msg: types.Message, state: FSMContext):
    text = get_template('questions.html', content_list=dict(answer_10={}, wrong_answer_10={}))
    if msg.text == '4':
        async with state.proxy() as data:
            data['banana_coins'] += 100
            data['test_finished'] = True
            await msg.answer(text['answer_10'])
    else:
        async with state.proxy() as data:
            data['banana_coins'] += 100
        await msg.answer(text['wrong_answer_10'])
    await asyncio.sleep(3)
    text = get_template('questions.html', content_list=dict(results={'sum': (await state.get_data())['banana_coins']}))
    await msg.answer(text['results'])
