from hashlib import md5
from aiogram import types
from .deps import app, bot, dp
from tortoise.transactions import in_transaction
from app.account import services as account_service
from app.dictionary.utm import services as utm_service


async def register_user(utm_id: str | None, msg: types.Message, usr: types.User):
    usr_hash: str = md5(f"{usr.id}-{usr.username}-{usr.full_name}".encode("utf8")).hexdigest()

    async with in_transaction(connection_name="default") as connection:
        user_id = await account_service.register_user(user_id=usr.id, user_hash=usr_hash, **msg.from_user.to_python())
        if utm_id:
            await utm_service.add_user(utm_id=utm_id, user_id=user_id)
