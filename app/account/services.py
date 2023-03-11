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


async def count_users_by_rank(rank: str) -> int:
    return await User.filter(rank=rank).count()


async def count_users_test_above_six() -> int:
    return await User.filter(coins__gt=500).count()


async def count_users_newbie_or_expert(newbie: bool) -> int:
    return await User.filter(newbie=newbie).count()
