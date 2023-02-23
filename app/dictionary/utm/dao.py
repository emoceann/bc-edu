from tortoise import Model, fields
from tortoise.fields import CASCADE


class UtmLabelDict(Model):
    """ Модель для траффик сорса """

    id = fields.UUIDField(pk=True)
    source = fields.CharField(max_length=256)
    medium = fields.CharField(max_length=256)
    campaign = fields.CharField(max_length=256)
    content = fields.IntField()


class UtmLabelM2mUser(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("account.User", related_name="user", on_delete=CASCADE)
    utm_label = fields.ForeignKeyField("dictionary_utm.UtmLabelDict", related_name='utmlabeldict', on_delete=CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
