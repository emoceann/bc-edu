from ._conftest import *
from app.statistics.models import StatisticModel
from app.statistics.services import StatisticModelBuilder
from app.integration.bizon365 import dao as i_bizon365_dao


@pytest.mark.anyio
async def test_statics_model(client: AsyncClient):
    report = json.load(open("report.json"))
    await i_bizon365_dao.WebinarRoom.create(
        id="123279:veb",
        title="Быстрый старт на рынке криптовалют",
        is_autowebinar=False,
        closest_date="2023-03-12T20:44:00.000Z",
        original_report=report
    )

    dump_statistics: StatisticModel = await StatisticModelBuilder().build()

    assert isinstance(dump_statistics.count_use_bot, int)
    assert dump_statistics.count_webinar_user is None
