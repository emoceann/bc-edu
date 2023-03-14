from tortoise import models, fields


class UserActions(models.Model):
    user = fields.ForeignKeyField('account.User', on_delete=fields.CASCADE)
    rank = fields.CharField(max_length=10)
    coins = fields.IntField()
    webinar_time = fields.CharField(max_length=12)

