from app.account.dao import User
from app.integration.bizon365 import dao, models
from app.dictionary.utm.dao import UtmLabelM2mUser

class BuildMetrics:
    result: dict[str, int] = {}
    restrict = ['build', 'result', 'get_results', 'restrict']

    async def get_results(self):
        await self.build()
        for i, v in self.result.items():
            setattr(self, i, v)
        return self

    async def build(self):
        for i in self.__dir__():
            if i in self.restrict or i.startswith('__'):
                continue
            func = getattr(self, i)
            res = await func()
            self.result[i[1:]] = res

    async def _bot_users_count(self):
        return await User.filter(is_admin=False).count()

    async def _webinar_users_count(self):
        count = 0
        for i in await dao.WebinarRoom.all().only('original_report'):
            res = models.ReportInsideModel.parse_obj(i.original_report['report'])
            count += len(res.report.rating)
        return count

    async def _order_amount(self):
        pass

    async def _income_amount(self):
        pass

    async def _reg_amount(self):
        return await UtmLabelM2mUser.all().count()

    async def _reg_target(self):
        return await UtmLabelM2mUser.exclude(utm_source='telegram').count()

    async def _reg_by_ref(self):
        pass

    async def _reg_by_tg(self):
        return await UtmLabelM2mUser.filter(utm_source='telegram').count()

    async def _webinar_users_by_first_hour(self):
        pass

    async def _webinar_users_by_second_hour(self):
        pass

    async def _webinar_users_by_third_hour(self):
        pass

    async def _webinar_banned_users(self):
        pass

    async def _webinar_redirect_to_alliance(self):
        pass

    async def _bot_users_newbie_count(self):
        return User.filter(newbie=True).count()

    async def _bot_users_experienced(self):
        return User.filter(experienced=True).count()

    async def _bot_users_ordered_count(self):
        pass

    async def _bot_users_membership_count(self):
        pass

    async def _bot_users_ref_count(self):
        pass

    async def _bot_referral_count(self):
        pass
