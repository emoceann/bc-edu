from tortoise import Model, fields


class UtmLabelDict(Model):
    """ Модель для траффик сорса """

    id = fields.UUIDField(pk=True)
    source = fields.CharField(max_length=256)
    medium = fields.CharField(max_length=256)
    campaign = fields.CharField(max_length=256)
    content = fields.IntField()


class BridgeUtmUser(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("account.User", related_name="user",
                                                                     on_delete=fields.CASCADE)
    utm_label: fields.ForeignKeyRelation["UtmLabelDict"] = fields.ForeignKeyField("dictionary_utm.UtmLabelDict",
                                                                                  related_name='utmlabeldict',
                                                                                  on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
