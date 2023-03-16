from .models import StatisticModel
from app.account import services as account_service
from app.integration.bizon365 import services as i_bizon365_service
from app.dictionary.utm import services as utmlabel_services
from app.integration.nowpayments import services as nowpayments_services


class StatisticModelBuilder(StatisticModel):

    async def _user_count_bot(self):
        self.count_user_bot = await account_service.find_count_users()
        self.count_users_newbie = await account_service.find_count_users_newbie_or_expert(newbie=True)
        self.count_users_expert = await account_service.find_count_users_newbie_or_expert(newbie=False)
        self.count_newbie_knowledge_base_red = await account_service.find_count_users_knowledgebase()
        self.count_newbie_test_finished = await account_service.find_count_users_test()
        self.count_users_test_above_six = await account_service.find_count_users_test_above_six()

    async def _webinar_report(self):
        if report := await i_bizon365_service.get_last_not_closed_report():
            self.count_webinar_user = len(report.report.rating)

            group_count_webinar_users_by_time = await i_bizon365_service.count_webinar_users_by_time(report.report)
            self.count_webinar_users_by_1_hour = group_count_webinar_users_by_time[1]
            self.count_webinar_users_by_2_hour = group_count_webinar_users_by_time[2]
            self.count_webinar_users_by_3_hour = group_count_webinar_users_by_time[3]

            self.count_webinar_users_ban = await i_bizon365_service.count_webinar_users_ban(report.report)

    async def _utmlabel_report(self):
        self.count_traffic_all = await utmlabel_services.count_reg_users_by_metric_or_all()
        self.count_traffic_target = await utmlabel_services.count_reg_user_by_target()
        self.count_traffic_telegram = await utmlabel_services.count_reg_users_by_metric_or_all(metric='telegram')

    async def _nowpayments_report(self):
        self.count_nowpayments_all = await nowpayments_services.nowpayments_count()

    async def build(self) -> StatisticModel:
        await self._utmlabel_report()
        await self._user_count_bot()
        await self._webinar_report()
        await self._nowpayments_report()
        return self
