import httpx
from .dao import *
from .models import *
from core.settings import settings
from core.logger import logger as log


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

