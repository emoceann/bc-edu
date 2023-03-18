from .models import UtmLabelRq
from .dao import UtmLabelDict, UtmLabelM2mUser
from tortoise.functions import Count
from tortoise.expressions import Q


async def get_utm_by(model: UtmLabelRq) -> UtmLabelDict | None:
    return await UtmLabelDict.get_or_none(
        source=model.source, medium=model.medium, campaign=model.campaign, content=model.content
    )


async def add_user(utm_id: str, user_id: int):
    await UtmLabelM2mUser.create(utm_label_id=utm_id, user_id=user_id)


async def count_reg_users_by_metric_or_all(metric: str = None) -> int:
    if metric:
        return await UtmLabelM2mUser.filter(utm_label__source=metric).count()
    return await UtmLabelM2mUser.all().count()


async def count_reg_user_by_target() -> int:
    return await UtmLabelM2mUser.exclude(utm_label__source='telegram').count()


async def get_utm_label_all():
    return await UtmLabelDict.all()


async def get_count_webinar_users_by_utmlabel(utm_id: str):
    query_result = await UtmLabelM2mUser.filter(utm_label=utm_id).annotate(webinar_count=Count('user__webinar_time', _filter=Q(user__webinar_time__isnull=False))).get_or_none()
    if webinar_count := query_result:
        return webinar_count.webinar_count
    return 0


async def get_count_users_by_utm_label(utm_id: str):
    return await UtmLabelM2mUser.filter(utm_label_id=utm_id).count()
