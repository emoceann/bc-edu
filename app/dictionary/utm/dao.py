from tortoise import Model, fields


class UtmLabelDict(Model):
    id = fields.UUIDField(pk=True)
    source = fields.CharField(max_length=256)
    medium = fields.CharField(max_length=256)
    campaign = fields.CharField(max_length=256)
    content = fields.IntField()
