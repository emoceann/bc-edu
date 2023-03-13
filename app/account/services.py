from tortoise.expressions import F
from datetime import datetime
from .dao import *


async def register_user(user_id: int, user_hash: str, **kwargs) -> int:
    if user := await User.get_or_none(id=user_id):
        if user.hash != user_hash:
            await User.filter(id=user_id).update(hash=user_hash, **kwargs)
    else:
        user = await User.create(hash=user_hash, **kwargs)
    return user.id


async def find_count_users() -> int:
    return await User.filter(is_admin=False).count()


async def find_count_users_by_rank(rank: str) -> int:
    return await User.filter(rank=rank).count()


async def find_count_users_test_above_six() -> int:
    return await User.filter(test=True, coins__gt=500).count()


async def find_count_users_newbie_or_expert(newbie: bool) -> int:
    return await User.filter(newbie=newbie).count()


async def find_count_users_test() -> int:
    return await User.filter(test_finished=True).count()


async def find_count_users_knowledgebase() -> int:
    return await User.filter(knowledgebase_red=True).count()


async def update_user_fields(user_id: int, data: dict):
    user = User.filter(id=user_id)
    if coins := data.pop('coins', None):
        await user.update(coins=F('coins') + coins)
    await user.update(**data, updated_at=datetime.utcnow())
