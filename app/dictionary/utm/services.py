from .models import UtmLabelRq
from .dao import UtmLabelDict, UtmLabelM2mUser


async def get_utm_by(model: UtmLabelRq) -> UtmLabelDict | None:
    return await UtmLabelDict.get_or_none(
        source=model.source, medium=model.medium, campaign=model.campaign, content=model.content
    )


async def add_user(utm_id: str, user_id: int):
    await UtmLabelM2mUser.create(utm_label_id=utm_id, user_id=user_id)
