from .models import StatisticModel
from app.account import services as account_service
from app.integration.bizon365 import services as i_bizon365_service


class StatisticModelBuilder(StatisticModel):

    async def _count_use_bot(self):
        self.count_use_bot = await account_service.find_count_users()

    async def _webinar_report(self):
        if report := await i_bizon365_service.get_last_not_closed_report():
            print(report)

    async def build(self) -> StatisticModel:
        await self._count_use_bot()
        await self._webinar_report()
        return self
