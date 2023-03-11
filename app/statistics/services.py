from .models import StatisticModel
from app.account import services as account_service
from app.integration.bizon365 import services as i_bizon365_service


class StatisticModelBuilder(StatisticModel):

    async def _count_use_bot(self):
        self.bot_users_count = await account_service.find_count_users()

    async def _webinar_report(self):
        if report := await i_bizon365_service.get_last_not_closed_report():
            self.count_webinar_user = len(report.report.rating)

            group_count_webinar_users_by_time = await i_bizon365_service.count_webinar_users_by_time(report.report)
            self.count_webinar_users_by_1_hour = group_count_webinar_users_by_time[1]
            self.count_webinar_users_by_2_hour = group_count_webinar_users_by_time[2]
            self.count_webinar_users_by_3_hour = group_count_webinar_users_by_time[3]

            self.count_webinar_users_ban = await i_bizon365_service.count_webinar_users_ban(report.report)

    async def build(self) -> StatisticModel:
        await self._count_use_bot()
        await self._webinar_report()
        return self
