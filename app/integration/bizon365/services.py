import httpx
from .dao import *
from .models import *
from core.settings import settings
from core.logger import logger as log
from datetime import datetime


async def webinars_get_subpages():
    """ Получение списка страниц регистрации и их рассылок """
    response: httpx.Response = httpx.get(
        url=f"{settings.BIZON365_API_HOST}/webinars/subpages/getSubpages?skip=0&limit=50",
        headers={"X-Token": settings.BIZON365_X_TOKEN}
    )
    assert response.status_code == 200, "Ошибка сервера Бизон365"
    response: dict = response.json()

    for room_id, room in response['rooms'].items():
        room, crt = await WebinarRoom.update_or_create(WebinarRoomModel(id=room_id, **room).dict())
        log.debug(f"{'Добавлена' if crt else 'Обновлена'} информация о комнате[{room.id}] - \"{room.title}\"")


async def webinars_refresh_reports():
    """ Получение список доступных отчетов и последующее обновление БД"""
    response: httpx.Response = httpx.get(
        url=f"{settings.BIZON365_API_HOST}/webinars/reports/getlist",
        headers={"X-Token": settings.BIZON365_X_TOKEN}
    )
    assert response.status_code == 200, "Ошибка сервера Бизон365"
    print(response.json())


async def webinars_get_detail_report(webinar_id: str):
    """ Получение детального отчета """
    response: httpx.Response = httpx.get(
        url=f"{settings.BIZON365_API_HOST}/webinars/reports/get?webinarId={webinar_id}",
        headers={"X-Token": settings.BIZON365_X_TOKEN}
    )
    assert response.status_code == 200, "Ошибка сервера Бизон365"
    print(response.json())


async def create_link_webinar(webinar: str, username: str, email: str, tg_id: str) -> str:
    """ Создание ссылки на вебинар """
    return f"{settings.BIZON365_BC_HOST}/room/{webinar}?email={email}&username={username}&cf_m_tg={tg_id}&autologin"


async def get_last_not_closed_report() -> ReportInsideModel | None:
    """ Получение следующего необработанного отчета """
    if query := await WebinarRoom.filter(close=False).order_by('closest_date').first().values('original_report'):
        return ReportInsideModel.parse_obj(query['original_report']['report'])


async def count_webinar_users_by_time(source: ReportInside):
    group_time: dict[int, int] = {1: 0, 2: 0, 3: 0}
    for user in source.usersMeta.values():
        millis: int = user['viewTill'] - user['view']
        hour: float = (millis / (1000 * 60 * 60)) % 24

        if 0 < hour < 1:
            group_time[1] += 1
        elif 1 < hour < 2:
            group_time[2] += 1
        else:
            group_time[3] += 1

    return group_time


async def count_webinar_users_ban(source: ReportInside) -> int:
    return len([user for user in source.usersMeta.values() if user.get('ban', False)])


async def get_last_webinar_title() -> str:
    webinar = await WebinarRoom.filter(close=False).order_by('closest_date').first().only('title')
    return webinar.title
