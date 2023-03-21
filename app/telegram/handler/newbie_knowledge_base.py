import asyncio
from app.telegram.deps import dp, bot
from app.telegram.handler.states import NewUser
from app.telegram.services import get_template
from aiogram import types
from aiogram.dispatcher import FSMContext
from app.account import services as account_services
from app.integration.bizon365 import services as bizon_services
from app.telegram.services import get_red_articles_user, red_article_user_write


@dp.message_handler(state=NewUser.newbie_knowledge_base)  # хендлер для новичка который не выбрал тесты
async def newbie_infobase(msg: types.Message, state: FSMContext):
    await account_services.update_user_fields(msg.from_user.id, {'coins': 100})
    text = get_template(
        'newbie_knowledge_base.html',
        content_list=dict(
            alliance_link={},
            stats={},
            buttons5={},
            text_knowledge2={
                'sum': (await state.get_data()).get('banana_coins', 0)},
            buttons2={},
            all_read={},
            button_all={}
        )
    )

    if msg.text == ' Потратить 100 Banana-coins🟡':
        await msg.reply(text['alliance_link'])
    if msg.text == 'Посмотреть результаты Banana Crypto Alliance📊':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(*(i for i in text['buttons5'].split('\n')))
        await msg.reply(text['stats'], reply_markup=markup)
        await NewUser.webinar_reg_start.set()
    if msg.text == 'Найти свой путь к Силе💪':
        article_count = len((await get_red_articles_user(msg.from_user.id)))
        webinar_title = await bizon_services.get_last_webinar_title()
        if article_count >= 8:
            await account_services.update_user_fields(msg.from_user.id, {'knowledgebase_red': True})
            message = text['all_read']
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            buttons = [i for i in text['button_all'].split('\n')]
            if not webinar_title:
                buttons.pop(2)
            await bot.send_message(msg.from_user.id, message, reply_markup=markup.add(*buttons))
        buttons = text['buttons2'].split('\n')[1:9]
        user_red = await get_red_articles_user(user_id=msg.from_user.id)
        if user_red:
            for i in user_red:
                for y in buttons:
                    if y.startswith(str(i.article_id)):
                        buttons.remove(y)
        markup = types.InlineKeyboardMarkup(
            row_width=1
        ).add(*(types.InlineKeyboardButton(i[1:], callback_data=i[:1]) for i in buttons))
        await msg.reply(text['text_knowledge2'], reply_markup=markup)
        await NewUser.newbie_articles_info.set()


@dp.callback_query_handler(state=NewUser.newbie_articles_info)
async def newbie_articles(callback: types.CallbackQuery, state: FSMContext):
    await red_article_user_write(user_id=callback.from_user.id, article_id=callback.data)
    webinar_title = await bizon_services.get_last_webinar_title()
    text = get_template(
        'newbie_knowledge_base.html',
        content_list=dict(
            buttons3={'choice': callback.data},
            notify={'webinar_title': webinar_title},
            buttons4={'webinar_title': webinar_title},
            continue_read={},
            all_read={}
        )
    )
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    await bot.send_message(callback.from_user.id, text['buttons3'])
    await asyncio.sleep(5)
    if not webinar_title:
        buttons = [i for i in text['buttons4'].split('\n')]
        buttons.pop(2)
        await bot.send_message(callback.from_user.id, 'Продолжай изучать базу знаний📜 либо присоединяйся к нашей крипто-братве 👊!', reply_markup=markup.add(*buttons))
    else:
        await bot.send_message(callback.from_user.id, text['notify'], reply_markup=markup.add(*(i for i in text['buttons4'].split('\n'))))
    await NewUser.newbie_knowledge_choose.set()


@dp.message_handler(state=NewUser.newbie_knowledge_choose)
async def newbie_knowledge_choose(msg: types.Message, state: FSMContext):
    article_count = len((await get_red_articles_user(msg.from_user.id)))
    webinar_title = await bizon_services.get_last_webinar_title()
    if msg.text == 'Продолжить изучение базы знаний📜':
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

    if msg.text == 'Посмотреть результаты Banana Crypto Alliance 📝':
        text = get_template('newbie_knowledge_base.html', content_list=dict(stats={}, buttons5={}))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*(i for i in text['buttons5'].split('\n')))
        await msg.reply(text['stats'], reply_markup=markup)
        await NewUser.webinar_reg_start.set()
