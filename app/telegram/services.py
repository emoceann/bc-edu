from .deps import app, bot, dp
from hashlib import md5
from app.account.dao import User
from app.dictionary.utm.dao import BridgeUtmUser, UtmLabelDict
from aiogram import types


async def register_new_user(message: types.Message):
    usr_hash: str = md5(f"{message.from_user.id}-{message.from_user.username}"
                        f"-{message.from_user.full_name}".encode("utf8")).hexdigest()
    user: User = await User.get_or_none(id=message.from_user.id)
    if not user:
        user = await User.create(hash=usr_hash, **message.from_user.to_python())
    elif user.hash != usr_hash:
        await User.filter(id=message.from_user.id).update(hash=usr_hash, **message.from_user.to_python())
    utm_id = message.text.split(' ')[1]
    print(user.id)
    await BridgeUtmUser.create(user_id=user.id, utm_label_id=utm_id)

