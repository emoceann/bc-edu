from tortoise import fields, Model


class BotUser(Model):
    id = fields.BigIntField(pk=True)
    hash = fields.CharField(max_length=255)
    username = fields.CharField(max_length=1024, null=True)
    full_name = fields.CharField(max_length=1024, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    language_code = fields.CharField(max_length=2, null=True)

    # traffic_link = fields.