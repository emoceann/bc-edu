import httpx
from .dao import *
from .deps import *
from .models import *
from core.settings import settings
from core.logger import logger as log


async def webinars_get_subpages():
    """ Получение списка страниц регистрации и их рассылок """
    response: httpx.Response = httpx.get(
        url="https://online.bizon365.ru/api/v1/webinars/subpages/getSubpages?skip=0&limit=50",
        headers={"X-Token": settings.BIZON365_X_TOKEN}
    )
    assert response.status_code == 200, "Ошибка сервера Бизон365"
    response: dict = response.json()

    for room_id, room in response['rooms'].items():
        room, crt = await WebinarRoom.update_or_create(WebinarRoomModel(id=room_id, **room).dict())
        log.debug(f"{'Добавлена' if crt else 'Обновлена'} информация о комнате[{room.id}] - \"{room.title}\"")


async def get_webinar_link(room: str, user_id: int) -> str:
    """ Отправляет ссылку на форму входа в комнату (автоматически подставлен userId) """
    return f"{settings.BIZON365_BC_HOST}/room/{room}?cf_m_tg={user_id}"

