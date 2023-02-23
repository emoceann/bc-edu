from .dao import UtmLabelDict
from .models import UtmLabelRq


async def get_utm_by(model: UtmLabelRq) -> UtmLabelDict | None:
    return await UtmLabelDict.get_or_none(
        source=model.source, medium=model.medium, campaign=model.campaign, content=model.content
    )
