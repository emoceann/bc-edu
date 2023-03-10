from ._conftest import *
from app.statistics.models import StatisticModel
from app.statistics.services import StatisticModelBuilder


@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    dump_statistics: StatisticModel = await StatisticModelBuilder().build()

    assert isinstance(dump_statistics.count_use_bot, int)
    assert dump_statistics.count_webinar_user is None
