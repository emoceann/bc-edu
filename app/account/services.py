from .dao import *


async def register_user(user_id: int, user_hash: str, **kwargs) -> int:
    if user := await User.get_or_none(id=user_id):
        if user.hash != user_hash:
            await User.filter(id=user_id).update(hash=user_hash, **kwargs)
    else:
        user = await User.create(hash=user_hash, **kwargs)
    return user.id
