from tortoise import models, fields
from aiogram.contrib.fsm_storage.memory import BaseStorage


class State(models.Model, BaseStorage):
    id = fields.UUIDField(pk=True)
    chat = fields.BigIntField(index=True)
    user = fields.BigIntField(index=True)
    state = fields.CharField(max_length=1024)
    data = fields.JSONField(null=True)
    bucket = fields.JSONField(null=True)

    async def close(self):
        pass

    async def wait_closed(self):
        pass

    async def get_state(self, *, chat=None, user=None, default=None) -> str | None:
        return await self.filter(chat=chat, user=user).first().only('state')

    async def get_data(self, *, chat=None, user=None, default=None) -> dict | None:
        return await self.filter(chat=chat, user=user).first().only('data')

    async def set_state(self, *, chat=None, user=None, state=None):
        pass

    async def set_data(self, *, chat=None, user=None, data=None):
        pass

    async def update_data(self, *, chat=None, user=None, data=None, **kwargs):
        pass

    async def get_bucket(self, *, chat=None, user=None, default=None) -> dict:
        pass

    async def set_bucket(self, *, chat=None, user=None, bucket=None):
        pass

    async def update_bucket(self, *, chat=None, user=None, bucket=None, **kwargs):
        pass
