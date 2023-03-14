from ._conftest import *
from app.telegram import services as tg_services


@pytest.mark.anyio
async def test_24_hours_not_active(client: AsyncClient):
    await tg_services.notify_24_hours()
