import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from app.telegram.deps import bot, dp, templates
from app.telegram.handler.states import NewUser
from app.telegram.services import register_user, get_template
from app.account import services as account_services


@dp.message_handler(commands='start', state='*')
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.finish()
    await register_user(utm_id=msg.get_args(), msg=msg, usr=msg.from_user)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    user = await account_services.get_user_by_fields(msg.from_user.id, 'test_finished', 'knowledgebase_red')
    if not user.test_finished or not user.knowledgebase_red:
        markup.add('Как долго я спал🥱?')
    await bot.send_photo(
        chat_id=msg.from_user.id,
        photo=open('static/telegram/tvoy_bilet.jpg', 'rb'),
        caption=templates.get_template('start.html').render(),
        reply_markup=markup.add('Взять билет!🎟️')
    )
    await NewUser.new_or_experienced.set()


@dp.message_handler(state=NewUser.new_or_experienced)
async def check_exp(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if msg.text == 'Взять билет!🎟️':
        await account_services.update_user_fields(msg.from_user.id, {'experienced': True})
        text = get_template('expirienced.html', content_list=dict(text_exp1={}))
        markup = markup.add('Подробнее о Альянсе')
        await msg.answer(text['text_exp1'], reply_markup=markup)
        await NewUser.experienced_info.set()
    if msg.text == 'Как долго я спал🥱?':
        text = get_template('newbie.html', content_list=dict(text1={}, text2={}))
        user = await account_services.get_user_by_fields(msg.from_user.id, 'test_finished', 'knowledgebase_red')
        if not user.test_finished:
            markup.add('Пройти испытание🏆')
        if not user.knowledgebase_red:
            markup.add('Изучить базу знаний📜')
        await account_services.update_user_fields(msg.from_user.id, {'newbie': True})
        await msg.answer(text['text1'])
        await asyncio.sleep(5)
        await NewUser.newbie.set()
        await msg.answer(text['text2'], reply_markup=markup)


@dp.message_handler(state=NewUser.newbie)
async def newbie_state(msg: types.Message, state: FSMContext):
    if msg.text == 'Изучить базу знаний📜':
        text = get_template(
            'newbie_knowledge_base.html',
            content_list=dict(
                text_knowledge={'sum': (await state.get_data()).get('coins', 0)},
                buttons1={}
            )
        )
        markup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(*(i for i in text['buttons1'].split('\n')))
        await msg.answer(text['text_knowledge'], reply_markup=markup)
        await NewUser.newbie_knowledge_base.set()
    if msg.text == 'Пройти испытание🏆':
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
