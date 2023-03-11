from .models import StatisticModel
from app.account import services as account_service


class StatisticModelBuilder(StatisticModel):

    async def _count_use_bot(self):
        self.bot_users_count = await account_service.find_count_users()

    async def build(self) -> StatisticModel:
        await self._count_use_bot()
        return self
