from tortoise import fields, Model


class User(Model):
    """ Модель юзера бота """

    id = fields.BigIntField(pk=True)
    hash = fields.CharField(max_length=255)
    username = fields.CharField(max_length=1024, null=True)
    full_name = fields.CharField(max_length=1024, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    language_code = fields.CharField(max_length=8, null=True)
    is_admin = fields.BooleanField(default=False)
    email = fields.CharField(max_length=255, null=True)
    phone_number = fields.CharField(max_length=16, null=True)
