from ._conftest import *
from app.telegram import services as tg_services


@pytest.mark.anyio
async def test_24_hours_not_active(client: AsyncClient):
    await tg_services.notify_24_hours()


@pytest.mark.anyio
async def test_webinar_start(client: AsyncClient):
    await tg_services.webinar_start_notify()


@pytest.mark.anyio
async def test_webinar_before_notify(client: AsyncClient):
    await tg_services.webinar_before_notify()
