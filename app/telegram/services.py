import re
from hashlib import md5
from aiogram import types
from jinja2 import Template
from .deps import app, bot, dp, templates
from tortoise.transactions import in_transaction
from app.account import services as account_service
from app.dictionary.utm import services as utm_service
from PIL import Image


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


async def phone_number_and_email_validator(phone_or_email: str):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", phone_or_email):
        return True
    elif re.match(r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", phone_or_email):
        return True
    return False