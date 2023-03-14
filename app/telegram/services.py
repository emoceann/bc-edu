import re
from hashlib import md5
from aiogram import types
from jinja2 import Template
from .deps import app, bot, dp, templates, storage
from tortoise.transactions import in_transaction
from app.account import services as account_service
from app.integration.bizon365 import services as bizon_services
from app.dictionary.utm import services as utm_service
from core.logger import logger as log


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


async def notify_24_hours():
    not_active = await account_service.get_not_active_users_24_hours('id', 'rank', 'test_finished')
    if not not_active:
        log.info('Не было неактивных юзеров за вчера')
        return

    text = get_template(
        'notify.html',
        content_list=dict(
            text={},
            buttons={'webinar_title': await bizon_services.get_last_webinar_title()}
        )
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(*(i for i in text['buttons'].split('\n')))
    for i in not_active:
        if not i.test_finished:
            markup.add('Пройти испытание и заработать Banana-coins')
        await bot.send_message(i.id, f"{text['text'] + i.rank}!", reply_markup=markup)
        await storage.set_state(chat=i.id, user=i.id, state=NewUser.notfiy_not_active)
    log.debug(f'{len(not_active)} - не активных пользователей были успешно уведомлены')
