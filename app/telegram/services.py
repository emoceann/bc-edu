import re
from datetime import datetime, timedelta
from hashlib import md5
from aiogram import types
from jinja2 import Template
from .deps import app, bot, dp, templates, storage
from app.telegram.handler.states import NewUser
from tortoise.transactions import in_transaction
from app.account import services as account_service
from app.integration.bizon365 import services as bizon_services
from app.dictionary.utm import services as utm_service
from core.logger import logger as log
from app.telegram.dao import RedArticleUser


async def register_user(utm_id: str | None, msg: types.Message, usr: types.User):
    usr_hash: str = md5(f"{usr.id}-{usr.username}-{usr.full_name}".encode("utf8")).hexdigest()

    async with in_transaction(connection_name="default") as connection:
        user_id = await account_service.register_user(user_id=usr.id, user_hash=usr_hash, **msg.from_user.to_python())
        if utm_id:
            await utm_service.add_user(utm_id=utm_id, user_id=user_id)


def get_template(name: str, content_list: dict[str, dict | None]) -> dict[str, str]:
    template: Template = templates.get_template(name)
    return dict(
        (key, u"".join(template.blocks[key](template.new_context(params)))) for key, params in content_list.items()
    )


def get_template_v1(name: str, content_list: dict[str, dict | None] | list) -> dict[str, str]:
    template: Template = templates.get_template(name)
    if isinstance(content_list, list):
        return dict((key, u"".join(template.blocks[key](template.new_context(None)))) for key in content_list)
    return dict(
        (key, u"".join(template.blocks[key](template.new_context(params)))) for key, params in content_list.items()
    )


async def email_validator(email: str):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):  # эмейл
        return True
    return False


async def phone_number_validator(phone: str):
    if re.match(r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", phone):  # номер телефона
        return True
    return False


async def get_rank(coins: int) -> str:
    if 0 < coins < 500:
        return 'Юнлинг'
    elif 500 < coins < 800:
        return 'Падаван'
    return 'Джедай'


async def notify_24_hours():
    not_active = await account_service.get_not_active_users_24_hours('id', 'rank', 'test_finished')
    if not not_active:
        log.info('Не было неактивных юзеров за вчера')
        return
    webinar_title = await bizon_services.get_last_webinar_title()
    text = get_template(
        'notify.html',
        content_list=dict(
            text={},
            buttons={'webinar_title': webinar_title}
        )
    )
    buttons1 = [i for i in text['buttons'].split('\n')]
    if not webinar_title:
        buttons1.pop(2)

    for i in not_active:
        buttons = buttons1[:]
        if i.test_finished:
            buttons = [i for i in buttons if i != buttons[3]]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(*buttons)
        await bot.send_message(i.id, f"{text['text'] + i.rank}!", reply_markup=markup)
        await storage.set_state(chat=i.id, user=i.id, state=NewUser.notfiy_not_active)
    log.debug(f'{len(not_active)} - неактивных пользователей были успешно уведомлены')


async def webinar_start_notify():
    today = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    webinar_users = await account_service.get_users_by_webinar_date(today)
    if not webinar_users:
        log.debug('Не было зарегестрированных пользователей на вебинар')
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Подключится')
    text = get_template('notify.html', content_list=dict(webinar_start={}))

    for i in webinar_users:
        await bot.send_message(i.id, text['webinar_start'], reply_markup=markup)
        await storage.set_state(user=i.id, chat=i.id, state=NewUser.webinar_start)

    log.debug(f'{len(webinar_users)} - Пользователей были успешно уведомлены о начале вебинара')


async def webinar_before_notify():
    today = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=3)
    webinar_users = await account_service.get_users_by_webinar_date_gt(today)
    if not webinar_users:
        log.debug('Не было зарегестрированных пользователей на вебинар')
        return
    count = 0
    text = get_template('notify.html', content_list=dict(before_12={}, before_3={}, before_1={}))
    for i in webinar_users:
        if (i.webinar_time.replace(tzinfo=None) - today) == timedelta(hours=12):
            await bot.send_message(i.id, text['before_12'])
        elif (i.webinar_time.replace(tzinfo=None) - today) == timedelta(hours=3):
            await bot.send_message(i.id, text['before_3'])
        elif (i.webinar_time.replace(tzinfo=None) - today) == timedelta(hours=1):
            await bot.send_message(i.id, text['before_1'])
        count += 1
    log.debug(f'{count} - зарегистрировавшиеся  пользователи были успешно уведомлены до начала вебинара')


async def get_red_articles_user(user_id: int):
    return await RedArticleUser.filter(user=user_id)

async def red_article_user_write(user_id: int, article_id: int):
    await RedArticleUser.create(user_id=user_id, article_id=article_id)