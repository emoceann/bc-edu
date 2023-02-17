from tortoise import Model, fields


class TrafficSource(Model):
    id = fields.BigIntField(pk=True)
    source = fields.CharField(max_length=256)
    medium = fields.CharField(max_length=256)
    campaign = fields.CharField(max_length=256)
    content = fields.BigIntField()


# class GeneratedLink(Model):
#     id = fields.BigIntField(pk=True)
#     uniq_link = fields.CharField(max_length=256, index=True)
#     users_count = fields.BigIntField()
