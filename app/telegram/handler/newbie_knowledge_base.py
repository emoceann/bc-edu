import asyncio
from app.telegram.deps import dp, bot
from app.telegram.handler.states import NewUser
from app.telegram.services import get_template
from aiogram import types
from aiogram.dispatcher import FSMContext
from app.account import services as account_services
from app.integration.bizon365 import services as bizon_services


@dp.message_handler(state=NewUser.newbie_knowledge_base)  # хендлер для новичка который не выбрал тесты
async def newbie_infobase(msg: types.Message, state: FSMContext):
    await account_services.update_user_fields(msg.from_user.id, {'coins': 100})
    text = get_template(
        'newbie_knowledge_base.html',
        content_list=dict(
            alliance_link={},
            text_knowledge2={
                'sum': (await state.get_data()).get('banana_coins', 0)},
            buttons2={}
        )
    )

    if msg.text == ' Потратить 100 Banana-coins':
        await msg.reply(text['alliance_link'])
    if msg.text == 'Посмотреть результаты Banana Crypto Alliance':
        await msg.reply('Результаты')
    if msg.text == 'Найти свой путь к Силе':
        buttons = text['buttons2'].split('\n')[1:9]
        markup = types.InlineKeyboardMarkup(
            row_width=1
        ).add(*(types.InlineKeyboardButton(i[1:], callback_data=i[:1]) for i in buttons))
        await msg.reply(text['text_knowledge2'], reply_markup=markup)
        await NewUser.newbie_articles_info.set()


@dp.callback_query_handler(state=NewUser.newbie_articles_info)
async def newbie_articles(callback: types.CallbackQuery, state: FSMContext):
    webinar_title = await bizon_services.get_last_webinar_title()
    text = get_template(
        'newbie_knowledge_base.html',
        content_list=dict(
            buttons3={'choice': callback.data},
            notify={'webinar_title': webinar_title},
            buttons4={'webinar_title': webinar_title}
        )
    )
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1).add(*(i for i in text['buttons4'].split('\n')))
    await bot.send_message(callback.from_user.id, text['buttons3'])
    await account_services.update_user_fields(callback.from_user.id, {'knowledgebase_red': True})
    await asyncio.sleep(10)
    await bot.send_message(callback.from_user.id, text['notify'], reply_markup=markup)
    await NewUser.newbie_knowledge_choose.set()


@dp.message_handler(state=NewUser.newbie_knowledge_choose)
async def newbie_knowledge_choose(msg: types.Message, state: FSMContext):
    text = get_template(
        'newbie_knowledge_base.html',
        content_list=dict(buttons2={})
    )
    if msg.text == 'Продолжить изучение базы знаний':
        buttons = text['buttons2'].split('\n')[1:9]
        markup = types.InlineKeyboardMarkup(
            row_width=1
        ).add(*(types.InlineKeyboardButton(i[1:], callback_data=i[:1]) for i in buttons))
        await msg.reply('База знаний', reply_markup=markup)
        await NewUser.newbie_articles_info.set()
    if msg.text.startswith('Зарегистрироваться на вебинар'):
        text = get_template(
            'webinar_reg.html',
            content_list=dict(
                webinar_info={},
                button_1={}
            )
        )
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(text['button_1'])
        await msg.answer(text['webinar_info'], reply_markup=markup)
        await NewUser.webinar_reg_start.set()
