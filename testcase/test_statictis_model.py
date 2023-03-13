from ._conftest import *
from app.statistics.models import StatisticModel
from app.statistics.services import StatisticModelBuilder
from app.integration.bizon365 import dao as i_bizon365_dao
from app.integration.bizon365 import services as bizon_services
from app.dictionary.utm import services as utmlabel_services


@pytest.mark.anyio
async def test_statics_model(client: AsyncClient):
    report = json.load(open("report.json"))
    await i_bizon365_dao.WebinarRoom.create(
        id="123279:veb",
        title="Быстрый старт на рынке криптовалют",
        is_autowebinar=False,
        closest_date="2023-03-12T20:44:00.000Z",
        original_report=report,
        close=False
    )

    dump_statistics: StatisticModel = await StatisticModelBuilder().build()

    assert isinstance(dump_statistics.count_user_bot, int)
    assert dump_statistics.count_webinar_user is 5


@pytest.mark.anyio
async def test_bizon_model_order_by(client: AsyncClient):
    assert isinstance(await bizon_services.get_last_webinar_title(), str)


@pytest.mark.anyio
async def test_utmlabelm2muser(client: AsyncClient):
    result = await utmlabel_services.count_reg_user_by_target()
    assert result is 1

